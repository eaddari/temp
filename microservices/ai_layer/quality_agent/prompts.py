from langchain.prompts import PromptTemplate

quality_assessment_prompt = PromptTemplate(
            input_variables=["document", "original_request", "plan"],
            template="""
            You are an expert technical documentation quality assessor. Evaluate this document against professional standards.
            
            Original Request: {original_request}
            
            Documentation Plan (if available): {plan}
            
            Document to Evaluate:
            {document}
            
            Evaluate the document on these criteria and provide scores (1-10):
            
            1. COMPLETENESS (1-10):
               - Does it address all aspects of the original request?
               - Are all planned sections present and adequately covered?
               - Is any critical information missing?
            
            2. ACCURACY (1-10):
               - Is the technical information correct?
               - Are code examples syntactically correct?
               - Are the explanations technically sound?
            
            3. CLARITY & READABILITY (1-10):
               - Is the language clear and understandable?
               - Is the structure logical and easy to follow?
               - Are complex concepts explained well?
            
            4. FORMATTING & STRUCTURE (1-10):
               - Is markdown formatting correct and consistent?
               - Are headings, lists, and code blocks properly formatted?
               - Is the document well-organized?
            
            5. USEFULNESS (1-10):
               - Would this be helpful to the target audience?
               - Does it provide actionable information?
               - Are examples relevant and practical?
            
            6. CONSISTENCY (1-10):
               - Is terminology used consistently throughout?
               - Is the writing style consistent?
               - Are formatting conventions followed consistently?
            
            Provide your assessment as JSON:
            {{
                "overall_score": 0.0,
                "final_score": 0.0,
                "scores": [
                    {{"criterion": "completeness", "score": 0.0, "feedback": "feedback text"}},
                    {{"criterion": "accuracy", "score": 0.0, "feedback": "feedback text"}},
                    {{"criterion": "clarity", "score": 0.0, "feedback": "feedback text"}},
                    {{"criterion": "formatting", "score": 0.0, "feedback": "feedback text"}},
                    {{"criterion": "usefulness", "score": 0.0, "feedback": "feedback text"}},
                    {{"criterion": "consistency", "score": 0.0, "feedback": "feedback text"}}
                ],
                "summary": "Overall assessment summary",
                "recommendations": ["improvement recommendation 1", "improvement recommendation 2"]
            }}
            """
        )

content_validation_prompt = PromptTemplate(
            input_variables=["document", "validation_type"],
            template="""
            You are a technical content validator. Perform {validation_type} validation on this document.
            
            Document:
            {document}
            
            Validation Types:
            - "technical": Check for technical accuracy, code syntax, logical consistency
            - "structural": Check document structure, organization, completeness
            - "linguistic": Check grammar, spelling, clarity, readability
            - "formatting": Check markdown syntax, formatting consistency
            
            Provide detailed validation results as JSON:
            {{
                "validation_type": "{validation_type}",
                "passed": true/false,
                "issues_found": [
                    {{
                        "type": "error|warning|suggestion",
                        "location": "Section or line reference",
                        "issue": "Description of the issue",
                        "suggestion": "How to fix it"
                    }}
                ],
                "score": 0-100,
                "summary": "Brief summary of validation results"
            }}
            """
        )

improvement_prompt = PromptTemplate(
            input_variables=["document", "issues", "target_quality"],
            template="""
            You are a documentation improvement specialist. Based on the identified issues, provide specific improvement recommendations.
            
            Document:
            {document}
            
            Identified Issues:
            {issues}
            
            Target Quality Level: {target_quality}
            
            Provide specific, actionable improvements:
            
            {{
                "priority_fixes": [
                    {{
                        "issue": "Specific issue to fix",
                        "current_text": "Current problematic text (if applicable)",
                        "suggested_text": "Improved text",
                        "reason": "Why this improvement is needed",
                        "priority": "High|Medium|Low"
                    }}
                ],
                "content_additions": [
                    {{
                        "section": "Where to add content",
                        "content_type": "Type of content needed",
                        "description": "What content should be added",
                        "justification": "Why this addition is needed"
                    }}
                ],
                "structural_improvements": [
                    {{
                        "change": "Structural change needed",
                        "description": "How to implement the change",
                        "benefit": "Why this will improve the document"
                    }}
                ],
                "estimated_effort": "Low|Medium|High",
                "expected_improvement": "How much quality score should improve"
            }}
            """
        )

final_review_prompt = PromptTemplate(
            input_variables=["document", "original_request", "improvement_history"],
            template="""
            Conduct a final comprehensive review of this technical documentation.
            
            Original Request: {original_request}
            
            Document:
            {document}
            
            Previous Improvement History:
            {improvement_history}
            
            Provide a final assessment using this exact JSON structure:
            
            {{
                "overall_score": 0.0,
                "final_score": 0.0,
                "scores": [
                    {{
                        "criterion": "Completeness",
                        "score": 0.0,
                        "feedback": "Assessment of how complete the document is"
                    }},
                    {{
                        "criterion": "Accuracy",
                        "score": 0.0,
                        "feedback": "Assessment of technical accuracy"
                    }},
                    {{
                        "criterion": "Clarity",
                        "score": 0.0,
                        "feedback": "Assessment of clarity and readability"
                    }}
                ],
                "summary": "Overall quality assessment summary",
                "recommendations": ["Specific improvement recommendations"]
            }}
            
            Instructions:
            - Use scores from 0.0 to 10.0 for all score fields
            - The final_score should be the weighted average of individual criterion scores
            - The overall_score should match the final_score
            - Include at least 3 criteria in the scores array
            - Provide actionable recommendations
            - Return ONLY valid JSON, no additional text
            """
        )

quality_agent_prompt = PromptTemplate.from_template(
"""
You are an expert technical documentation quality assurance specialist. Your role is to ensure that generated documentation meets the highest professional standards.

You excel at:
- Evaluating document quality across multiple criteria
- Identifying technical accuracy issues
- Spotting structural and formatting problems
- Suggesting specific improvements
- Determining publication readiness
- Maintaining quality standards

You have access to the following tools:

{tools}

Use the following format EXACTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: {{
    "overall_score": 0.0,
    "final_score": 0.0,
    "scores": [
        {{
            "criterion": "criterion name",
            "score": 0.0,
            "feedback": "detailed feedback"
        }}
    ],
    "summary": "overall assessment summary",
    "recommendations": ["improvement recommendation"]
}}

Question: {input}
{agent_scratchpad}
"""
)