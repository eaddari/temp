# microservices.ai_layer.quality_agent

Source file: `microservices\ai_layer\quality_agent.py`

## Source Code

```python
import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any, List
import json
import re
from datetime import datetime

load_dotenv()

# Initialize LLM for quality checking
llm = AzureChatOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    temperature=0.2  # Low temperature for consistent evaluation
)

class DocumentQualityAgent:
    def __init__(self, llm):
        self.llm = llm
        
        # Quality assessment prompt
        self.quality_assessment_prompt = PromptTemplate(
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
                "criteria_scores": {{
                    "completeness": 0,
                    "accuracy": 0,
                    "clarity": 0,
                    "formatting": 0,
                    "usefulness": 0,
                    "consistency": 0
                }},
                "strengths": ["List of document strengths"],
                "weaknesses": ["List of specific issues found"],
                "critical_issues": ["Issues that must be fixed"],
                "suggestions": ["Specific improvement recommendations"],
                "missing_sections": ["Sections that should be added"],
                "quality_level": "Excellent|Good|Acceptable|Needs Improvement|Poor"
            }}
            """
        )
        
        # Content validation prompt
        self.content_validation_prompt = PromptTemplate(
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
        
        # Improvement suggestion prompt
        self.improvement_prompt = PromptTemplate(
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
        
        # Final review prompt
        self.final_review_prompt = PromptTemplate(
            input_variables=["document", "original_request", "improvement_history"],
            template="""
            Conduct a final comprehensive review of this technical documentation.
            
            Original Request: {original_request}
            
            Document:
            {document}
            
            Previous Improvement History:
            {improvement_history}
            
            Provide a final assessment:
            
            {{
                "ready_for_publication": true/false,
                "final_score": 0-100,
                "certification_level": "Production Ready|Needs Minor Fixes|Requires Major Revision|Not Ready",
                "final_recommendations": ["Last-minute suggestions"],
                "sign_off_notes": "Professional assessment summary",
                "target_audience_suitability": "How well it serves the intended audience",
                "maintenance_notes": ["Notes for future updates"]
            }}
            """
        )
    
    def assess_quality(self, document: str, original_request: str = "", plan: str = "") -> Dict[str, Any]:
        """Comprehensive quality assessment of the document."""
        try:
            assessment_chain = self.quality_assessment_prompt | self.llm | StrOutputParser()
            result = assessment_chain.invoke({
                "document": document,
                "original_request": original_request,
                "plan": plan
            })
            
            result = self._clean_json_response(result)
            assessment = json.loads(result)
            
            # Calculate overall score from criteria scores
            if "criteria_scores" in assessment:
                scores = assessment["criteria_scores"]
                overall = sum(scores.values()) / len(scores)
                assessment["overall_score"] = round(overall, 1)
            
            return assessment
            
        except Exception as e:
            print(f"Error in quality assessment: {e}")
            return self._create_fallback_assessment()
    
    def validate_content(self, document: str, validation_types: List[str] = None) -> Dict[str, Any]:
        """Validate specific aspects of the document content."""
        if validation_types is None:
            validation_types = ["technical", "structural", "linguistic", "formatting"]
        
        validation_results = {}
        
        for validation_type in validation_types:
            try:
                validation_chain = self.content_validation_prompt | self.llm | StrOutputParser()
                result = validation_chain.invoke({
                    "document": document,
                    "validation_type": validation_type
                })
                
                result = self._clean_json_response(result)
                validation_results[validation_type] = json.loads(result)
                
            except Exception as e:
                print(f"Error in {validation_type} validation: {e}")
                validation_results[validation_type] = {
                    "validation_type": validation_type,
                    "passed": False,
                    "issues_found": [{"type": "error", "issue": f"Validation failed: {str(e)}"}],
                    "score": 0,
                    "summary": f"Validation error occurred"
                }
        
        return validation_results
    
    def suggest_improvements(self, document: str, issues: List[Dict], target_quality: str = "Excellent") -> Dict[str, Any]:
        """Generate specific improvement suggestions based on identified issues."""
        try:
            improvement_chain = self.improvement_prompt | self.llm | StrOutputParser()
            result = improvement_chain.invoke({
                "document": document,
                "issues": json.dumps(issues, indent=2),
                "target_quality": target_quality
            })
            
            result = self._clean_json_response(result)
            improvements = json.loads(result)
            
            return improvements
            
        except Exception as e:
            print(f"Error generating improvements: {e}")
            return {"priority_fixes": [], "content_additions": [], "structural_improvements": []}
    
    def final_review(self, document: str, original_request: str = "", improvement_history: str = "") -> Dict[str, Any]:
        """Conduct final comprehensive review for publication readiness."""
        try:
            review_chain = self.final_review_prompt | self.llm | StrOutputParser()
            result = review_chain.invoke({
                "document": document,
                "original_request": original_request,
                "improvement_history": improvement_history
            })
            
            result = self._clean_json_response(result)
            review = json.loads(result)
            
            return review
            
        except Exception as e:
            print(f"Error in final review: {e}")
            return {
                "ready_for_publication": False,
                "final_score": 0,
                "certification_level": "Not Ready",
                "sign_off_notes": f"Review failed due to error: {str(e)}"
            }
    
    def comprehensive_quality_check(self, document: str, original_request: str = "", plan: str = "") -> Dict[str, Any]:
        """Run a complete quality check workflow."""
        print("🔍 Starting comprehensive quality check...")
        
        # Step 1: Quality Assessment
        print("📊 Assessing overall quality...")
        quality_assessment = self.assess_quality(document, original_request, plan)
        
        # Step 2: Content Validation
        print("✅ Validating content...")
        validation_results = self.validate_content(document)
        
        # Step 3: Collect issues for improvement suggestions
        all_issues = []
        for validation_type, results in validation_results.items():
            all_issues.extend(results.get("issues_found", []))
        
        # Add issues from quality assessment
        if "critical_issues" in quality_assessment:
            for issue in quality_assessment["critical_issues"]:
                all_issues.append({"type": "critical", "issue": issue, "location": "General"})
        
        # Step 4: Generate improvements if needed
        improvements = {}
        overall_score = quality_assessment.get("overall_score", 0)
        if overall_score < 8.0 or all_issues:
            print("💡 Generating improvement suggestions...")
            improvements = self.suggest_improvements(document, all_issues)
        
        # Step 5: Final review
        print("📋 Conducting final review...")
        final_review = self.final_review(document, original_request)
        
        # Compile comprehensive results
        comprehensive_results = {
            "timestamp": datetime.now().isoformat(),
            "quality_assessment": quality_assessment,
            "validation_results": validation_results,
            "improvements": improvements,
            "final_review": final_review,
            "summary": {
                "overall_score": overall_score,
                "total_issues": len(all_issues),
                "critical_issues": len([i for i in all_issues if i.get("type") == "critical"]),
                "ready_for_publication": final_review.get("ready_for_publication", False),
                "certification_level": final_review.get("certification_level", "Unknown")
            }
        }
        
        return comprehensive_results
    
    def _clean_json_response(self, response: str) -> str:
        """Clean LLM response to extract valid JSON."""
        # Remove markdown code blocks
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*$', '', response)
        
        # Find JSON content between braces
        start = response.find('{')
        end = response.rfind('}') + 1
        
        if start != -1 and end > start:
            return response[start:end]
        
        return response.strip()
    
    def _create_fallback_assessment(self) -> Dict[str, Any]:
        """Create a basic fallback assessment when automated assessment fails."""
        return {
            "overall_score": 5.0,
            "criteria_scores": {
                "completeness": 5,
                "accuracy": 5,
                "clarity": 5,
                "formatting": 5,
                "usefulness": 5,
                "consistency": 5
            },
            "strengths": ["Assessment could not be completed automatically"],
            "weaknesses": ["Manual review required"],
            "critical_issues": ["Automated assessment failed"],
            "suggestions": ["Perform manual quality review"],
            "missing_sections": [],
            "quality_level": "Needs Review"
        }

# Initialize the quality agent
quality_agent = DocumentQualityAgent(llm)

# Tool functions
def assess_document_quality(document_text: str) -> str:
    """Assess the overall quality of a document across multiple criteria."""
    try:
        assessment = quality_agent.assess_quality(document_text)
        return json.dumps(assessment, indent=2)
    except Exception as e:
        return f"Error assessing quality: {str(e)}"

def validate_document_content(document_text: str) -> str:
    """Validate document content for technical accuracy, structure, and formatting."""
    try:
        validation = quality_agent.validate_content(document_text)
        return json.dumps(validation, indent=2)
    except Exception as e:
        return f"Error validating content: {str(e)}"

def suggest_document_improvements(document_text: str) -> str:
    """Generate specific suggestions for improving the document quality."""
    try:
        # First assess to find issues
        assessment = quality_agent.assess_quality(document_text)
        issues = []
        
        # Convert assessment issues to improvement format
        for issue in assessment.get("critical_issues", []):
            issues.append({"type": "critical", "issue": issue})
        for issue in assessment.get("weaknesses", []):
            issues.append({"type": "weakness", "issue": issue})
        
        improvements = quality_agent.suggest_improvements(document_text, issues)
        return json.dumps(improvements, indent=2)
    except Exception as e:
        return f"Error generating improvements: {str(e)}"

def final_quality_review(document_text: str) -> str:
    """Conduct a final comprehensive review for publication readiness."""
    try:
        review = quality_agent.final_review(document_text)
        return json.dumps(review, indent=2)
    except Exception as e:
        return f"Error in final review: {str(e)}"

def comprehensive_quality_check(document_text: str) -> str:
    """Run a complete quality check workflow including all validation steps."""
    try:
        results = quality_agent.comprehensive_quality_check(document_text)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error in comprehensive check: {str(e)}"

# Define tools for the quality agent
quality_tools = [
    Tool(
        name="AssessQuality",
        func=assess_document_quality,
        description="Assess overall document quality with scores for completeness, accuracy, clarity, formatting, usefulness, and consistency."
    ),
    Tool(
        name="ValidateContent",
        func=validate_document_content,
        description="Validate document content for technical accuracy, structural integrity, linguistic quality, and formatting correctness."
    ),
    Tool(
        name="SuggestImprovements",
        func=suggest_document_improvements,
        description="Generate specific, actionable suggestions for improving document quality based on identified issues."
    ),
    Tool(
        name="FinalReview",
        func=final_quality_review,
        description="Conduct final comprehensive review to determine publication readiness and certification level."
    ),
    Tool(
        name="ComprehensiveCheck",
        func=comprehensive_quality_check,
        description="Run complete quality assurance workflow including assessment, validation, improvements, and final review."
    )
]

# Agent prompt for the quality agent
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
Final Answer: the final answer to the original input question

IMPORTANT: You MUST end with "Final Answer:" followed by your response.

Question: {input}
{agent_scratchpad}
"""
)

# Create the quality agent executor
quality_agent_executor = create_react_agent(llm, quality_tools, quality_agent_prompt)
quality_agent_runner = AgentExecutor(
    agent=quality_agent_executor,
    tools=quality_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

if __name__ == "__main__":
    print("🔍 Documentation Quality Assurance Agent")
    print("=" * 50)
    
    # Test with a sample document
    sample_document = """
# API Documentation

## Overview
This API provides functionality for managing users.

## Endpoints

### GET /users
Returns a list of users.

**Response:**
```json
{
  "users": []
}
```

### POST /users
Creates a new user.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```
"""
    
    print("\n🧪 Testing quality assessment on sample document...")
    print("-" * 50)
    
    try:
        # Test comprehensive quality check
        print("🔍 Running comprehensive quality check...")
        results = quality_agent.comprehensive_quality_check(sample_document)
        
        # Display summary
        summary = results.get("summary", {})
        print(f"\n📊 Quality Summary:")
        print(f"Overall Score: {summary.get('overall_score', 'N/A')}/10")
        print(f"Total Issues: {summary.get('total_issues', 'N/A')}")
        print(f"Critical Issues: {summary.get('critical_issues', 'N/A')}")
        print(f"Ready for Publication: {summary.get('ready_for_publication', 'N/A')}")
        print(f"Certification Level: {summary.get('certification_level', 'N/A')}")
        
        # Display key findings
        quality_assessment = results.get("quality_assessment", {})
        if quality_assessment.get("strengths"):
            print(f"\n✅ Strengths:")
            for strength in quality_assessment["strengths"][:3]:  # Show top 3
                print(f"  • {strength}")
        
        if quality_assessment.get("weaknesses"):
            print(f"\n⚠️  Areas for Improvement:")
            for weakness in quality_assessment["weaknesses"][:3]:  # Show top 3
                print(f"  • {weakness}")
        
        # Show validation summary
        validation_results = results.get("validation_results", {})
        print(f"\n🔍 Validation Results:")
        for validation_type, result in validation_results.items():
            score = result.get("score", 0)
            status = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
            print(f"  {validation_type.title()}: {score}/100 {status}")
        
    except Exception as e:
        print(f"❌ Error in testing: {e}")
    
    # Interactive mode
    print("\n" + "="*50)
    print("Interactive Mode - Enter document text for quality check (type 'exit' to quit):")
    print("💡 Tip: You can paste multi-line documents, end with 'END' on a new line")
    
    while True:
        try:
            print("\n📝 Enter document text (type 'END' on new line to finish, 'exit' to quit):")
            
            lines = []
            while True:
                line = input()
                if line.strip().lower() == 'exit':
                    exit()
                if line.strip() == 'END':
                    break
                lines.append(line)
            
            if not lines:
                print("❌ No document text provided.")
                continue
            
            document_text = '\n'.join(lines)
            
            print(f"\n🔄 Analyzing document quality ({len(document_text)} characters)...")
            
            # Run comprehensive quality check
            results = quality_agent.comprehensive_quality_check(document_text)
            
            print("\n" + "="*80)
            print("🔍 QUALITY ASSESSMENT REPORT")
            print("="*80)
            
            # Display summary
            summary = results.get("summary", {})
            print(f"📊 Overall Score: {summary.get('overall_score', 'N/A')}/10")
            print(f"🎯 Certification: {summary.get('certification_level', 'N/A')}")
            print(f"📋 Total Issues: {summary.get('total_issues', 'N/A')}")
            print(f"🚨 Critical Issues: {summary.get('critical_issues', 'N/A')}")
            print(f"✅ Publication Ready: {summary.get('ready_for_publication', 'N/A')}")
            
            # Quality breakdown
            quality_assessment = results.get("quality_assessment", {})
            criteria_scores = quality_assessment.get("criteria_scores", {})
            
            if criteria_scores:
                print(f"\n📈 Quality Breakdown:")
                for criterion, score in criteria_scores.items():
                    bar = "█" * (score // 2) + "░" * (5 - score // 2)
                    print(f"  {criterion.title():15} [{bar}] {score}/10")
            
            # Show strengths and weaknesses
            if quality_assessment.get("strengths"):
                print(f"\n✅ Strengths:")
                for strength in quality_assessment["strengths"]:
                    print(f"  • {strength}")
            
            if quality_assessment.get("weaknesses"):
                print(f"\n⚠️  Weaknesses:")
                for weakness in quality_assessment["weaknesses"]:
                    print(f"  • {weakness}")
            
            if quality_assessment.get("critical_issues"):
                print(f"\n🚨 Critical Issues:")
                for issue in quality_assessment["critical_issues"]:
                    print(f"  • {issue}")
            
            # Show improvement suggestions if available
            improvements = results.get("improvements", {})
            if improvements.get("priority_fixes"):
                print(f"\n💡 Priority Fixes:")
                for fix in improvements["priority_fixes"][:3]:  # Show top 3
                    priority_emoji = "🔴" if fix.get('priority') == 'High' else "🟡" if fix.get('priority') == 'Medium' else "🟢"
                    print(f"  {priority_emoji} {fix.get('issue', 'N/A')}")
                    if fix.get('suggested_text'):
                        print(f"     Suggested: {fix['suggested_text'][:100]}...")
            
            # Final review
            final_review = results.get("final_review", {})
            if final_review.get("sign_off_notes"):
                print(f"\n📋 Final Assessment:")
                print(f"  {final_review['sign_off_notes']}")
            
            print("="*80)
            
            # Ask if user wants to save the report
            save = input("\n💾 Would you like to save this quality report? (y/n): ")
            if save.lower() == 'y':
                filename = input("Enter filename (without extension): ")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_filename = f"{filename}_quality_report_{timestamp}.json"
                
                with open(report_filename, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2)
                print(f"✅ Quality report saved as {report_filename}")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

```
