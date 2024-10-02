from .config import DEG_LIST

def get_degree_info(plan_title):
    title = plan_title
    plan_degree_type = "Unknown"
    plan_degree = "Unknown"
    if title.startswith("Bachelor"):
        plan_degree_type = "Bachelor"
    elif title.startswith("Certificate"):
        plan_degree_type = "Certificate"
    elif title.startswith("Doctor"):
        plan_degree_type = "Doctor"
    elif title.startswith("Graduate Diploma"):
        plan_degree_type = "Graduate Diploma"
    elif title.startswith("Master"):
        plan_degree_type = "Master"
    elif title.startswith("No Qualification"):
        plan_degree_type = "No Qualification"
    elif title.startswith("Postgraduate Certificate") or title.startswith("Post Graduate Certificate"):
        plan_degree_type = "Postgraduate Certificate"
    elif title.startswith("Postgraduate Diploma"):
        plan_degree_type = "Postgraduate Diploma"
    elif title.startswith("Professional Doctorate"):
        plan_degree_type = "Professional Doctorate"
    else:
        print(f'"{title}" has unknown degree type.')

    for degree in DEG_LIST:
        if title.startswith(degree):
            plan_degree = degree
            break
    else:
        print(f'"{title}" has unknown degree.')
    
    return {
        'degreeType': plan_degree_type,
        'degree': plan_degree
    }


def get_fields_from_schema(schema):
    text_fields = []
    obj_fields = []
    for property, spec in schema['properties'].items():
        if spec['type'] == 'string':
            text_fields.append(property)
        elif spec['type'] in ['array', 'object']:
            obj_fields.append(property)
        else:
            ValueError("We shouldn't have types other than string, array and object.")
    all_fields = text_fields + obj_fields
    return text_fields, obj_fields, all_fields