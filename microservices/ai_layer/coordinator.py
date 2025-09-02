import os
from dotenv import load_dotenv
from typing import Dict, Any
import json
from datetime import datetime
from planning_agent import planning_agent
from query_agent import agent_executor as query_agent
from generation_agent import generation_agent
from quality_agent import quality_agent

load_dotenv()

class DocumentationCoordinator:
    """Minimal coordinator that orchestrates all agents to generate documentation."""
    
    def __init__(self):
        self.planning_agent = planning_agent
        self.query_agent = query_agent
        self.generation_agent = generation_agent
        self.quality_agent = quality_agent
        
    def generate_documentation(self, user_request: str, quality_threshold: float = 7.0) -> Dict[str, Any]:
        """Coordinate all agents to generate high-quality documentation."""
        
        try:
            # Step 1: Planning
            plan = self.planning_agent.create_documentation_plan(user_request)
            if not plan or "sections" not in plan:
                raise Exception("Planning failed")
            
            # Step 2: Data Collection
            collected_data = {}
            for section in plan.get("sections", []):
                section_name = section.get("section_name", "Unknown")
                queries = section.get("queries", [])
                
                section_data = []
                for query in queries:
                    try:
                        response = self.query_agent.invoke({"input": query})
                        section_data.append({
                            "query": query,
                            "result": response.get("output", ""),
                            "success": True
                        })
                    except Exception:
                        section_data.append({
                            "query": query,
                            "result": "Query failed",
                            "success": False
                        })
                
                collected_data[section_name] = section_data
            
            # Step 3: Document Generation
            document = self.generation_agent.generate_document(user_request)
            if not document:
                document = self._create_fallback_document(plan, collected_data, user_request)
            
            # Step 4: Quality Check
            quality_results = self.quality_agent.comprehensive_quality_check(
                document, user_request, json.dumps(plan, indent=2)
            )
            
            final_score = quality_results.get("summary", {}).get("overall_score", 0)
            
            return {
                "success": True,
                "document": document,
                "quality_score": final_score,
                "plan": plan,
                "quality_details": quality_results,
                "meets_threshold": final_score >= quality_threshold
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "document": None,
                "quality_score": 0
            }
    
    def _create_fallback_document(self, plan: Dict[str, Any], data: Dict[str, Any], user_request: str) -> str:
        """Create basic document when generation agent fails."""
        doc_info = plan.get("document_info", {})
        title = doc_info.get("title", f"Documentation for: {user_request}")
        
        parts = [f"# {title}\n\n## Introduction\n{user_request}\n"]
        
        for section in plan.get("sections", []):
            section_name = section.get("section_name", "Section")
            parts.append(f"\n## {section_name}\n")
            
            section_data = data.get(section_name, [])
            for item in section_data:
                if item.get("success", False):
                    parts.append(f"**Query**: {item['query']}\n\n{item['result']}\n\n")
        
        return "".join(parts)

# Initialize coordinator
coordinator = DocumentationCoordinator()

def main():
    """Simple main interface."""
    print("🤖 AI Documentation Generator")
    
    user_input = input("Enter your documentation request: ").strip()
    if not user_input:
        print("No request provided")
        return
    
    print("⏳ Generating...")
    result = coordinator.generate_documentation(user_input)
    
    if result["success"]:
        document = result["document"]
        score = result["quality_score"]
        
        print(f"✅ Generated (Quality: {score}/10)")
        
        filename = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(document)
        print(f"📄 Saved as {filename}")
        
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
    
    def _generate_document_from_plan(self, plan: Dict[str, Any], data: Dict[str, Any], user_request: str) -> str:
        """Generate documentation using the generation agent."""
        try:
            # Use the generation agent to create the document
            document = self.generation_agent.generate_document(user_request)
            return document
        except Exception as e:
            # Fallback: create a basic document from the plan and data
            return self._create_fallback_document(plan, data, user_request)
    
    def _quality_improvement_loop(self, document: str, user_request: str, plan: Dict[str, Any], 
                                quality_threshold: float, max_iterations: int) -> tuple[str, Dict[str, Any]]:
        """Run quality improvement iterations until threshold is met or max iterations reached."""
        
        current_document = document
        iteration = 0
        improvement_history = []
        
        while iteration < max_iterations:
            iteration += 1
            
            # Run comprehensive quality check
            quality_results = self.quality_agent.comprehensive_quality_check(
                current_document, user_request, json.dumps(plan, indent=2)
            )
            
            current_score = quality_results.get("summary", {}).get("overall_score", 0)
            
            if current_score >= quality_threshold:
                break
            
            improvements = quality_results.get("improvements", {})
            if not improvements.get("priority_fixes"):
                break
            
            improvement_history.append({
                "iteration": iteration,
                "score_before": current_score,
                "suggestions": improvements
            })
            
            # break per far finire il quality check
            break
        
        final_quality = self.quality_agent.comprehensive_quality_check(
            current_document, user_request, json.dumps(plan, indent=2)
        )
        
        quality_metrics = {
            "final_score": final_quality.get("summary", {}).get("overall_score", 0),
            "iterations_run": iteration,
            "threshold_met": final_quality.get("summary", {}).get("overall_score", 0) >= quality_threshold,
            "certification_level": final_quality.get("final_review", {}).get("certification_level", "Unknown"),
            "ready_for_publication": final_quality.get("final_review", {}).get("ready_for_publication", False),
            "improvement_history": improvement_history
        }
        
        return current_document, quality_metrics
    
    def quick_generate(self, user_request: str) -> str:
        """Quick generation with minimal quality checks for fast results."""
        try:
            document = self.generation_agent.generate_document(user_request)
            return document
        except Exception as e:
            return f"# Error\n\nFailed to generate documentation: {str(e)}"
    
    def _create_fallback_document(self, plan: Dict[str, Any], data: Dict[str, Any], user_request: str) -> str:
        """Create a basic fallback document when the generation agent fails."""
        doc_info = plan.get("document_info", {})
        title = doc_info.get("title", f"Documentation for: {user_request}")
        
        document_parts = [f"# {title}\n"]
        
        # Add introduction
        document_parts.append("## Introduction\n")
        document_parts.append(f"This document was generated based on the request: {user_request}\n")
        
        # Add sections
        for section in plan.get("sections", []):
            section_name = section.get("section_name", "Section")
            document_parts.append(f"\n## {section_name}\n")
            
            # Add section data
            section_data = data.get(section_name, [])
            for item in section_data:
                if item.get("success", False):
                    document_parts.append(f"### Query Results\n")
                    document_parts.append(f"**Query**: {item['query']}\n")
                    document_parts.append(f"**Result**: {item['result']}\n")
        
        return "\n".join(document_parts)
    
    def save_workflow_result(self, workflow_result: Dict[str, Any], filename: str = None) -> str:
        """Save the complete workflow result to files."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"documentation_workflow_{timestamp}"
        
        # Save the document
        doc_filename = f"{filename}.md"
        with open(doc_filename, "w", encoding="utf-8") as f:
            f.write(workflow_result.get("final_document", ""))
        
        # Save the workflow metadata
        meta_filename = f"{filename}_metadata.json"
        with open(meta_filename, "w", encoding="utf-8") as f:
            # Create a clean copy without the document content for metadata
            metadata = workflow_result.copy()
            metadata["final_document"] = f"Saved to {doc_filename}"
            json.dump(metadata, f, indent=2)
        
        return doc_filename

coordinator = DocumentationCoordinator()

def main():
    """Main interface for the documentation generation system."""
    
    print("🤖 AI Documentation Generation System")
    print("=" * 60)
    print("Multi-Agent Workflow: Planning → Data Collection → Generation → Quality Assurance")
    print("\nCommands:")
    print("  📝 generate <request>    - Full quality documentation generation")
    print("  ⚡ quick <request>       - Quick generation (minimal quality checks)")
    print("  📊 status               - Show system status")
    print("  🔧 config               - Show configuration")
    print("  ❌ exit/quit            - Exit the system")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n🤖 DocGen> ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'status':
                print("✅ All agents loaded and ready")
                print("📊 Available agents: Planning, Query, Generation, Quality")
                continue
            
            if user_input.lower() == 'config':
                print("🔧 Configuration:")
                print(f"  Neo4j URI: {os.getenv('NEO4J_URI', 'Not set')}")
                print(f"  Azure OpenAI: {os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')}")
                print(f"  Model: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'Not set')}")
                continue
            
            if user_input.startswith('generate '):
                request = user_input[9:].strip()
                if not request:
                    print("❌ Please provide a documentation request")
                    continue
                
                print(f"\n🚀 Starting full documentation generation...")
                result = coordinator.generate_documentation(request)
                
                if result["success"]:
                    print(f"\n✅ SUCCESS!")
                    print(f"📊 Quality Score: {result['quality_metrics'].get('final_score', 'N/A')}/10")
                    print(f"⏱️  Total Time: {result.get('total_duration', 0):.1f}s")
                    
                    # Ask if user wants to save
                    save = input("\n💾 Save documentation? (y/n): ").lower()
                    if save == 'y':
                        filename = input("Enter filename (optional): ").strip()
                        coordinator.save_workflow_result(result, filename if filename else None)
                    
                    # Show preview
                    preview = input("\n👀 Show document preview? (y/n): ").lower()
                    if preview == 'y':
                        doc = result.get("final_document", "")
                        print("\n" + "="*80)
                        print("📄 DOCUMENT PREVIEW")
                        print("="*80)
                        print(doc[:1000] + ("..." if len(doc) > 1000 else ""))
                        print("="*80)
                else:
                    print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
                
                continue
            
            if user_input.startswith('quick '):
                request = user_input[6:].strip()
                if not request:
                    print("❌ Please provide a documentation request")
                    continue
                
                print(f"\n⚡ Starting quick generation...")
                document = coordinator.quick_generate(request)
                
                # Show preview
                print("\n" + "="*80)
                print("📄 QUICK DOCUMENT")
                print("="*80)
                print(document[:1000] + ("..." if len(document) > 1000 else ""))
                print("="*80)
                
                # Ask if user wants to save
                save = input("\n💾 Save document? (y/n): ").lower()
                if save == 'y':
                    filename = input("Enter filename: ").strip()
                    if filename:
                        with open(f"{filename}.md", "w", encoding="utf-8") as f:
                            f.write(document)
                        print(f"✅ Document saved as {filename}.md")
                
                continue
            
            if user_input.strip():
                print(f"\n🚀 Starting documentation generation for: {user_input}")
                result = coordinator.generate_documentation(user_input)
                
                if result["success"]:
                    print(f"\n✅ SUCCESS!")
                    print(f"📊 Quality Score: {result['quality_metrics'].get('final_score', 'N/A')}/10")
                    
                    # Show preview
                    doc = result.get("final_document", "")
                    print("\n" + "="*60)
                    print("📄 GENERATED DOCUMENTATION")
                    print("="*60)
                    print(doc[:800] + ("..." if len(doc) > 800 else ""))
                    print("="*60)
                else:
                    print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
            else:
                print("❌ Please enter a documentation request or command")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
