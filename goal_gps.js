const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs');
const path = require('path');

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(''); // Replace with your actual API key

async function getGoalRecommendation(goal, duration, risk) {
    try {
        // Read SBI Life insurance schemes data
        const schemesPath = path.join(__dirname, 'sbilife_policies.txt');
        let schemesData = '';
        
        try {
            schemesData = fs.readFileSync(schemesPath, 'utf8');
        } catch (fileError) {
            console.log('SBI schemes file not found, proceeding without it');
            schemesData = 'No specific insurance schemes data available.';
        }

        // Define the JSON schema for structured output
        const schema = {
            type: "object",
            properties: {
                color: {
                    type: "string",
                    enum: ["Green", "Yellow", "Red"]
                },
                reason: {
                    type: "string"
                }
            },
            required: ["color", "reason"]
        };

        // Initialize model with structured output configuration
        const model = genAI.getGenerativeModel({
            model: 'gemini-1.5-flash',
            generationConfig: {
                responseMimeType: "application/json",
                responseSchema: schema,
            },
        });

        const prompt = `
You are a strict financial advisor analyzing financial goals. You must be precise and realistic in your assessment.

User's Financial Goal:
- Goal: ${goal}
- Duration: ${duration} months
- Risk Appetite: ${risk}

Available SBI Life Insurance Schemes:
${schemesData}

STRICT CLASSIFICATION RULES - Follow these exactly:

**RED INDICATORS (immediately classify as RED if ANY apply):**
1. Duration > 480 months (40+ years) for ANY goal - this is unrealistic planning
2. Duration < 12 months for major purchases (house/car) without sufficient existing savings
3. Completely unrealistic timelines (like 600 months = 50 years for a car)
4. Goal amount vs duration math doesn't work even with high returns
5. Insurance products fundamentally unsuitable for the goal type and timeline

**GREEN INDICATORS (classify as GREEN only if ALL apply):**
1. Duration between 12-360 months (1-30 years) for major goals
2. Timeline aligns with typical financial planning horizons
3. Suitable SBI Life schemes available that match risk appetite
4. Realistic monthly savings requirement vs typical income
5. Goal-timeline combination is financially sound

**YELLOW INDICATORS (everything else):**
1. Goal is achievable but needs strategy adjustment
2. Timeline needs minor modification
3. Risk appetite doesn't perfectly match available schemes
4. Requires combination of insurance + other investments

SPECIFIC GOAL ANALYSIS:

For HOUSE purchases:
- 12-240 months: Potentially GREEN if realistic
- 240-360 months: Usually YELLOW (too long term)
- >360 months or <12 months: RED

For CAR purchases:
- <12 months: RED (insufficient planning time)
- 12-60 months: Potentially GREEN
- >240 months: RED (unrealistic for a depreciating asset)

For EDUCATION:
- 36-180 months: Potentially GREEN
- <36 months or >300 months: RED

For RETIREMENT:
- 120-480 months: Potentially GREEN
- <120 months or >480 months: RED

CALCULATION CHECK:
If goal requires more than 50% of typical middle-class income as monthly savings, classify as RED.

Your response must include:
1. Clear mathematical reasoning
2. Specific scheme recommendation (if applicable)
3. Why the timeline is/isn't realistic
4. Alternative suggestions if RED/YELLOW

BE DECISIVE. Don't default to YELLOW. Use RED for clearly unrealistic scenarios and GREEN for well-planned achievable goals.
The response (from the assessment) should have only 4-5 lines.
`;
        
        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        console.log('Raw Gemini Output:', text);

        // Parse the JSON response
        const recommendation = JSON.parse(text);
        
        // Validate the response structure
        if (!recommendation.color || !recommendation.reason) {
            throw new Error('Invalid recommendation structure');
        }

        // Ensure color is one of the expected values
        if (!['Green', 'Yellow', 'Red'].includes(recommendation.color)) {
            throw new Error(`Invalid color value: ${recommendation.color}`);
        }

        console.log('Parsed recommendation:', recommendation);
        return recommendation;

    } catch (error) {
        console.error('Goal GPS Error:', error);
        throw error;
    }
}

module.exports = {
    getGoalRecommendation
};
