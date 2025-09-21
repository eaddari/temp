generation_input = f"Generate useful content for the section: current_section\n"
user_message = f"User request: state['user_request']\n"
sections_for_context = f"Sections for context: sections"


input = generation_input+user_message+sections_for_context
print(input)

lines = input.split('\n')
print(lines)
    
current_section_name = lines[0].replace("Generate useful content for the section: ", "").strip()
print(current_section_name)
query_prompt = f"Find information relevant for '{current_section_name}' in the documentation"

print(query_prompt)