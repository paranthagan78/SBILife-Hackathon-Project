# Enhanced policy_recommend.py with better classification

import sys
import os
import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import unicodedata
import re
import json
import traceback
import numpy as np
import subprocess
import tempfile
from typing import Dict

def get_user_data(username):
    """Get user data from database with better error handling"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'users.db')
        
        if not os.path.exists(db_path):
            print(f"Database file not found at: {db_path}", file=sys.stderr)
            return None
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        if cursor.fetchone()[0] == 0:
            print(f"User {username} not found in database", file=sys.stderr)
            conn.close()
            return None
            
        cursor.execute("""
            SELECT gender, age, marital_status, salary, balance
            FROM users
            WHERE username = ?
        """, (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return {
                'gender': user_data[0] or 'Unknown',
                'age': user_data[1] or 25,
                'marital_status': user_data[2] or 'Single',
                'salary': user_data[3] or 50000,
                'balance': user_data[4] or 10000
            }
        return None
    except Exception as e:
        print(f"Database error: {str(e)}", file=sys.stderr)
        return None

def clean_text(text):
    """Clean text with better error handling"""
    try:
        text = str(text)
        text = unicodedata.normalize('NFKD', text)
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    except Exception as e:
        print(f"Text cleaning error: {str(e)}", file=sys.stderr)
        return str(text).lower()

def create_policy_categories():
    """Create rule-based policy categories for better matching"""
    return {
        'high_risk': ['term', 'ulip', 'market', 'equity', 'growth', 'investment'],
        'low_risk': ['traditional', 'endowment', 'guaranteed', 'assured', 'savings'],
        'long_term': ['pension', 'retirement', 'child', 'education', 'future'],
        'short_term': ['money back', 'immediate', 'quick', 'liquidity'],
        'family': ['child', 'family', 'education', 'marriage', 'dependent'],
        'retirement': ['pension', 'retirement', 'annuity', 'senior', 'old age']
    }

def categorize_user_query(user_input):
    """Categorize user query based on keywords"""
    user_input_lower = user_input.lower()
    categories = create_policy_categories()
    matched_categories = []
    
    for category, keywords in categories.items():
        if any(keyword in user_input_lower for keyword in keywords):
            matched_categories.append(category)
    
    return matched_categories

def load_and_prepare_data():
    """Load and prepare the Excel data with enhanced processing"""
    try:
        excel_path = os.path.join(os.path.dirname(__file__), 'sbilife.xlsx')
        
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel file not found at: {excel_path}")
            
        df = pd.read_excel(excel_path)
        
        required_columns = ['Policies', 'WhyGet', 'Desc']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Clean and process data
        df['Policies'] = df['Policies'].apply(clean_text)
        df['WhyGet'] = df['WhyGet'].fillna('').apply(clean_text)
        df['Desc'] = df['Desc'].fillna('').apply(clean_text)
        
        # Create combined text for better feature extraction
        df['Combined_Text'] = df['Policies'] + ' ' + df['WhyGet'] + ' ' + df['Desc']
        
        # Create policy categories based on keywords
        df['Category'] = df['Combined_Text'].apply(lambda x: get_policy_category(x))
        
        policy_descriptions = dict(zip(df['Policies'], df['WhyGet']))
        
        label_encoder = LabelEncoder()
        df['Policy_Label'] = label_encoder.fit_transform(df['Policies'])
        
        return df, policy_descriptions, label_encoder
    except Exception as e:
        print(f"Data loading error: {str(e)}", file=sys.stderr)
        raise

def get_policy_category(policy_text):
    """Assign category to policy based on its description"""
    policy_text = policy_text.lower()
    
    if any(word in policy_text for word in ['pension', 'retirement', 'annuity']):
        return 'retirement'
    elif any(word in policy_text for word in ['term', 'protection', 'cover']):
        return 'protection'
    elif any(word in policy_text for word in ['ulip', 'investment', 'growth', 'market']):
        return 'investment'
    elif any(word in policy_text for word in ['child', 'education', 'future']):
        return 'child'
    elif any(word in policy_text for word in ['money back', 'return', 'liquidity']):
        return 'savings'
    else:
        return 'general'
    
def enhanced_policy_matching(user_input, df, policy_descriptions):
    """Enhanced policy matching using multiple approaches - Updated for array return"""
    try:
        # Approach 1: Rule-based matching
        user_categories = categorize_user_query(user_input)
        rule_based_matches = []
        
        if user_categories:
            for category in user_categories:
                if category == 'high_risk':
                    matches = df[df['Combined_Text'].str.contains('ulip|investment|market|growth', case=False, na=False)]
                elif category == 'low_risk':
                    matches = df[df['Combined_Text'].str.contains('traditional|endowment|guaranteed|assured', case=False, na=False)]
                elif category == 'long_term':
                    matches = df[df['Combined_Text'].str.contains('pension|retirement|child|education', case=False, na=False)]
                elif category == 'retirement':
                    matches = df[df['Combined_Text'].str.contains('pension|retirement|annuity', case=False, na=False)]
                else:
                    continue
                
                if not matches.empty:
                    rule_based_matches.extend(matches.to_dict('records'))
        
        # Return rule-based match if found
        if rule_based_matches:
            # Sort by relevance and take the best match
            best_match = rule_based_matches[0]
            return {
                'name': best_match['Policies'],
                'why': policy_descriptions.get(best_match['Policies'], 'No description available'),
                'confidence': 0.8,  # High confidence for rule-based matches
                'method': 'rule_based'
            }
        
        # Approach 2: Semantic similarity (fallback)
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000, min_df=1, ngram_range=(1, 2))
        policy_vectors = vectorizer.fit_transform(df['Combined_Text'])
        user_vector = vectorizer.transform([user_input])
        
        similarities = cosine_similarity(user_vector, policy_vectors)[0]
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        if best_similarity > 0.1:  # Minimum similarity threshold
            best_match = df.iloc[best_match_idx]
            return {
                'name': best_match['Policies'],
                'why': policy_descriptions.get(best_match['Policies'], 'No description available'),
                'confidence': float(best_similarity),
                'method': 'semantic_similarity'
            }
        
        # Final fallback: return most general policy
        fallback_policy = df.iloc[0]
        return {
            'name': fallback_policy['Policies'],
            'why': policy_descriptions.get(fallback_policy['Policies'], 'No description available'),
            'confidence': 0.3,
            'method': 'fallback'
        }
        
    except Exception as e:
        print(f"Enhanced matching error: {str(e)}", file=sys.stderr)
        
def predict_policy_enhanced(user_input, username, df, policy_descriptions):
    """Enhanced policy prediction with multiple approaches - Returns array format with Trust AI Shield"""
    try:
        # Get user data if available
        user_data = get_user_data(username) if username else None
        
        # Enhance user input with user data and context
        enhanced_input = user_input
        if user_data:
            age_group = "young" if user_data['age'] < 30 else "middle-aged" if user_data['age'] < 50 else "senior"
            income_group = "high" if user_data['salary'] > 100000 else "medium" if user_data['salary'] > 50000 else "low"
            
            enhanced_input += f" {age_group} {income_group} income {user_data['gender']} {user_data['marital_status']}"
        
        # Use enhanced matching
        result = enhanced_policy_matching(enhanced_input, df, policy_descriptions)
        
        if result:
            # Convert single result to array format expected by frontend
            policy_array = [{
                'name': result['name'],
                'why': result['why']
            }]
            
            policy_result = {
                'policies': policy_array,  # Frontend expects 'policies' array
                'confidence': result.get('confidence', 0.5),
                'method': result.get('method', 'enhanced'),
                'enhanced_query': enhanced_input,
                'user_data_used': user_data is not None,
                'user_profile': user_data
            }
            
            # Enhance with Trust AI Shield
            return enhance_with_trust_ai(policy_result, user_data)
        
        # Fallback to original approach if enhanced matching fails
        return predict_policy_original(user_input, username, df, policy_descriptions)
        
    except Exception as e:
        print(f"Enhanced prediction error: {str(e)}", file=sys.stderr)
        return {'error': f"Enhanced prediction failed: {str(e)}"}

def predict_policy_original(user_input, username, df, policy_descriptions):
    """Original prediction method as fallback - Returns array format with Trust AI Shield"""
    try:
        user_data = get_user_data(username) if username else None
        
        enhanced_input = user_input
        if user_data:
            enhanced_input = f"{user_input}. "
            enhanced_input += f"I am a {user_data['age']} year old {user_data['gender']}. "
            enhanced_input += f"I am {user_data['marital_status']}. "
            enhanced_input += f"My annual salary is {user_data['salary']} and I have a balance of {user_data['balance']}."
        
        # Use TF-IDF and Random Forest
        vectorizer = TfidfVectorizer(stop_words='english', max_features=500, min_df=1)
        X = vectorizer.fit_transform(df['Combined_Text'].astype(str))
        y = df['Policy_Label']
        
        classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        classifier.fit(X, y)
        
        user_vector = vectorizer.transform([enhanced_input])
        prediction = classifier.predict(user_vector)
        probabilities = classifier.predict_proba(user_vector)[0]
        
        label_encoder = LabelEncoder()
        label_encoder.fit(df['Policies'])
        policy_name = label_encoder.inverse_transform(prediction)[0]
        confidence = max(probabilities)
        
        # Return in array format expected by frontend
        policy_array = [{
            'name': policy_name,
            'why': policy_descriptions.get(policy_name, 'No description available')
        }]
        
        policy_result = {
            'policies': policy_array,  # Frontend expects 'policies' array
            'confidence': float(confidence),
            'enhanced_query': enhanced_input,
            'user_data_used': user_data is not None,
            'method': 'machine_learning'
        }
        
        # Enhance with Trust AI Shield
        return enhance_with_trust_ai(policy_result, user_data)
        
    except Exception as e:
        print(f"Original prediction error: {str(e)}", file=sys.stderr)
        return {'error': f"Original prediction failed: {str(e)}"}
    
def get_policy_description_from_excel(policy_name):
    """Get policy description from Excel file"""
    try:
        excel_path = os.path.join(os.path.dirname(__file__), 'sbilife.xlsx')
        df = pd.read_excel(excel_path)
        
        # Find matching policy
        matching_row = df[df['Policies'].str.lower() == policy_name.lower()]
        if not matching_row.empty:
            desc = matching_row.iloc[0].get('Desc', '')
            why_get = matching_row.iloc[0].get('WhyGet', '')
            return f"{desc} {why_get}".strip()
        
        return ""
    except Exception as e:
        print(f"Error getting policy description: {str(e)}", file=sys.stderr)
        return ""
    
def enhance_with_trust_ai(policy_result: Dict, user_profile: Dict) -> Dict:
    """
    Enhance policy recommendation with Trust AI Shield verification
    """
    try:
        print(f"[TRUST AI] Starting Trust AI Shield verification...", file=sys.stderr)
        
        # Skip trust verification if no policies to verify
        if not policy_result.get('policies') or len(policy_result.get('policies', [])) == 0:
            policy_result['trust_verification_enabled'] = False
            print(f"[TRUST AI] No policies to verify, skipping trust verification", file=sys.stderr)
            return policy_result
        
        enhanced_policies = []
        
        # Process each policy through Trust AI Shield
        for policy in policy_result.get('policies', []):
            try:
                print(f"[TRUST AI] Processing policy: {policy.get('name')}", file=sys.stderr)
                
                # Prepare user data for trust prediction (matching trust_policy.py format)
                user_data = {
                    'username': user_profile.get('username', 'unknown') if user_profile else 'unknown',
                    'credit_score': user_profile.get('credit_score', 650) if user_profile else 650,
                    'geography': user_profile.get('geography', 'Unknown') if user_profile else 'Unknown',
                    'gender': user_profile.get('gender', 'Unknown') if user_profile else 'Unknown',
                    'age': user_profile.get('age', 35) if user_profile else 35,
                    'marital_status': user_profile.get('marital_status', 'Single') if user_profile else 'Single',
                    'salary': user_profile.get('salary', 50000) if user_profile else 50000,
                    'tenure': user_profile.get('tenure', 2) if user_profile else 2,
                    'balance': user_profile.get('balance', 100000) if user_profile else 100000,
                    'num_products': user_profile.get('num_products', 1) if user_profile else 1,
                    'has_credit_card': user_profile.get('has_credit_card', 0) if user_profile else 0,
                    'is_active': user_profile.get('is_active', 1) if user_profile else 1,
                    'exited': user_profile.get('exited', 0) if user_profile else 0
                }

                excel_path = r'C:\Users\paran\OneDrive\Desktop\SBI Final\new-approach\sbilife.xlsx'
                
                # Prepare policy data for trust prediction
                # NEW - Get real policy classification:
                from trust_policy import PolicyClassifierAndTrustCalculator
                classifier = PolicyClassifierAndTrustCalculator(excel_path)

                # Get policy description (you might need to add this function)
                policy_desc = get_policy_description_from_excel(policy.get('name', ''))

                # Get enhanced trust scores
                enhanced_scores = classifier.get_enhanced_trust_scores(
                    policy_name=policy.get('name', ''),
                    policy_description=policy_desc,
                    user_profile=user_data
                )

                policy_data = {
                    'name': policy.get('name'),
                    'type': enhanced_scores['policy_type'],
                    'transparency_score': enhanced_scores['transparency_score'],
                    'suitability_score': enhanced_scores['suitability_score'],
                    'financial_safety_score': enhanced_scores['financial_safety_score'],
                    'compliance_score': enhanced_scores['compliance_score']
                }
                
                print(f"[TRUST AI] User data prepared: {user_data}", file=sys.stderr)
                print(f"[TRUST AI] Policy data prepared: {policy_data}", file=sys.stderr)
                
                # Call Trust AI Shield analyzer
                trust_script_path = os.path.join(os.path.dirname(__file__), 'trust_policy.py')
                print(f"[TRUST AI] Calling trust script: {trust_script_path}", file=sys.stderr)
                
                trust_process = subprocess.run([
                    sys.executable,
                    trust_script_path,
                    json.dumps(user_data),
                    json.dumps(policy_data)
                ], capture_output=True, text=True, cwd=os.path.dirname(__file__), timeout=30)
                
                print(f"[TRUST AI] Trust process return code: {trust_process.returncode}", file=sys.stderr)
                print(f"[TRUST AI] Trust process stdout: {trust_process.stdout}", file=sys.stderr)
                print(f"[TRUST AI] Trust process stderr: {trust_process.stderr}", file=sys.stderr)
                
                if trust_process.returncode == 0 and trust_process.stdout.strip():
                    try:
                        trust_result = json.loads(trust_process.stdout.strip())
                        
                        if trust_result.get('success'):
                            # Enhance policy with trust information
                            enhanced_policy = {
                                'name': policy.get('name'),
                                'why': policy.get('why'),
                                'trust_score': trust_result.get('trust_score', 0.7),
                                'trust_confidence': trust_result.get('confidence_level', 'Medium'),
                                'trust_interpretation': trust_result.get('interpretation', {
                                    'level': 'Medium Trust',
                                    'description': 'Trust assessment completed',
                                    'recommendation': 'Review Carefully'
                                }),
                                'trust_model_used': trust_result.get('model_used', 'Trust AI Shield'),
                                'trust_timestamp': trust_result.get('prediction_timestamp')
                            }
                            enhanced_policies.append(enhanced_policy)
                            print(f"[TRUST AI] ✅ Trust verification successful for policy: {policy.get('name')}", file=sys.stderr)
                        else:
                            # Trust verification failed, use default trust values
                            enhanced_policy = {
                                'name': policy.get('name'),
                                'why': policy.get('why'),
                                'trust_score': 0.7,
                                'trust_confidence': 'Medium',
                                'trust_interpretation': {
                                    'level': 'Medium Trust',
                                    'description': f'Trust verification failed: {trust_result.get("error", "Unknown error")}',
                                    'recommendation': 'Review Carefully'
                                },
                                'trust_error': trust_result.get('error', 'Unknown error')
                            }
                            enhanced_policies.append(enhanced_policy)
                            print(f"[TRUST AI] ❌ Trust verification failed for policy {policy.get('name')}: {trust_result.get('error')}", file=sys.stderr)
                    except json.JSONDecodeError as je:
                        print(f"[TRUST AI] ❌ Trust result JSON parse error for {policy.get('name')}: {je}", file=sys.stderr)
                        print(f"[TRUST AI] Raw trust output: {trust_process.stdout}", file=sys.stderr)
                        # Use default trust values
                        enhanced_policy = {
                            'name': policy.get('name'),
                            'why': policy.get('why'),
                            'trust_score': 0.7,
                            'trust_confidence': 'Medium',
                            'trust_interpretation': {
                                'level': 'Medium Trust',
                                'description': 'Trust verification parsing failed',
                                'recommendation': 'Review Carefully'
                            },
                            'trust_error': f'JSON parse error: {str(je)}'
                        }
                        enhanced_policies.append(enhanced_policy)
                else:
                    print(f"[TRUST AI] ❌ Trust process failed for {policy.get('name')}: return code {trust_process.returncode}", file=sys.stderr)
                    print(f"[TRUST AI] Trust stderr: {trust_process.stderr}", file=sys.stderr)
                    # Use default trust values
                    enhanced_policy = {
                        'name': policy.get('name'),
                        'why': policy.get('why'),
                        'trust_score': 0.7,
                        'trust_confidence': 'Medium',
                        'trust_interpretation': {
                            'level': 'Medium Trust',
                            'description': 'Trust verification process failed',
                            'recommendation': 'Review Carefully'
                        },
                        'trust_error': f'Process failed with code {trust_process.returncode}: {trust_process.stderr}'
                    }
                    enhanced_policies.append(enhanced_policy)
                    
            except subprocess.TimeoutExpired:
                print(f"[TRUST AI] ⏰ Trust verification timeout for policy: {policy.get('name')}", file=sys.stderr)
                # Use default trust values for timeout
                enhanced_policy = {
                    'name': policy.get('name'),
                    'why': policy.get('why'),
                    'trust_score': 0.7,
                    'trust_confidence': 'Medium',
                    'trust_interpretation': {
                        'level': 'Medium Trust',
                        'description': 'Trust verification timed out after 30 seconds',
                        'recommendation': 'Review Carefully'
                    },
                    'trust_error': 'Timeout after 30 seconds'
                }
                enhanced_policies.append(enhanced_policy)
            except Exception as pe:
                print(f"[TRUST AI] ❌ Trust verification error for {policy.get('name')}: {str(pe)}", file=sys.stderr)
                print(f"[TRUST AI] Error traceback: {traceback.format_exc()}", file=sys.stderr)
                # Use default trust values for any other error
                enhanced_policy = {
                    'name': policy.get('name'),
                    'why': policy.get('why'),
                    'trust_score': 0.7,
                    'trust_confidence': 'Medium',
                    'trust_interpretation': {
                        'level': 'Medium Trust',
                        'description': f'Trust verification error: {str(pe)}',
                        'recommendation': 'Review Carefully'
                    },
                    'trust_error': str(pe)
                }
                enhanced_policies.append(enhanced_policy)
        
        # Update policy result with enhanced policies
        if enhanced_policies:
            policy_result['policies'] = enhanced_policies
            policy_result['trust_verification_enabled'] = True
            policy_result['trust_verification_timestamp'] = pd.Timestamp.now().isoformat()
            print(f"[TRUST AI] ✅ Trust AI Shield verification completed for {len(enhanced_policies)} policies", file=sys.stderr)
        else:
            policy_result['trust_verification_enabled'] = False
            print(f"[TRUST AI] ❌ No policies were enhanced with trust verification", file=sys.stderr)
        
        return policy_result
        
    except Exception as e:
        print(f"[TRUST AI] ❌ Trust AI Shield integration error: {str(e)}", file=sys.stderr)
        print(f"[TRUST AI] ❌ Trust AI Shield traceback: {traceback.format_exc()}", file=sys.stderr)
        
        # Return original result if trust verification fails completely
        policy_result['trust_verification_enabled'] = False
        policy_result['trust_verification_error'] = str(e)
        return policy_result

def main():
    """Main function with comprehensive error handling"""
    try:
        if len(sys.argv) < 2:
            # Test mode
            print("No arguments provided. Running test mode...", file=sys.stderr)
            test_cases = [
                "Give me a high risk policy",
                "I need a long term policy", 
                "Suggest a pension plan",
                "I want term insurance",
                "Child education policy"
            ]
            
            df, policy_descriptions, label_encoder = load_and_prepare_data()
            print(f"Loaded {len(df)} policies from Excel", file=sys.stderr)
            
            for test_case in test_cases:
                print(f"\nTesting: {test_case}", file=sys.stderr)
                result = predict_policy_enhanced(test_case, "test_user", df, policy_descriptions)
                print(json.dumps(result, indent=2))
            return
        
        # Parse arguments
        if len(sys.argv) == 2:
            # Single argument could be user description or JSON data
            arg = sys.argv[1]
            try:
                # Try parsing as JSON first
                data = json.loads(arg)
                user_description = data.get('description', '')
                username = data.get('username')
            except json.JSONDecodeError:
                # Treat as plain description
                user_description = arg
                username = None
        else:
            user_description = sys.argv[1]
            username = sys.argv[2] if len(sys.argv) > 2 else None
        
        print(f"Processing request for user: {username}", file=sys.stderr)
        print(f"User description: {user_description}", file=sys.stderr)
        
        # Load and prepare data
        df, policy_descriptions, label_encoder = load_and_prepare_data()
        print(f"Loaded {len(df)} policies from Excel", file=sys.stderr)
        
        # Make prediction using enhanced method
        result = predict_policy_enhanced(user_description, username, df, policy_descriptions)
        
        # Output result as JSON
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    main()
