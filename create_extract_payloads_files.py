import os
import shutil
import zipfile
from jinja2 import Environment, FileSystemLoader

template_dir = 'templates'
env = Environment(loader=FileSystemLoader(template_dir))

template_name = 'lambda_function.py.tpl'
template = env.get_template(template_name)

context = [
    {   'table': 'competition_details',
        'lambda_name': 'extract_competition_details_lambda',
        'extractor_file_name': 'competition_details_extractor',
        'extractor_class': 'CompetitionDetailsExtractor',
        'extractor_get_method': 'get_competition_details'
    },
    {
        'table': 'matches',
        'lambda_name': 'extract_matches_lambda',
        'extractor_file_name': 'matches_extractor',
        'extractor_class': 'MatchesExtractor',
        'extractor_get_method': 'get_matches'
    },
    {
        'table': 'standings',
        'lambda_name': 'extract_standings_lambda',
        'extractor_file_name': 'standings_extractor',
        'extractor_class': 'StandingsExtractor',
        'extractor_get_method': 'get_standings'
    },
    {
        'table': 'teams',
        'lambda_name': 'extract_teams_lambda',
        'extractor_file_name': 'teams_extractor',
        'extractor_class': 'TeamsExtractor',
        'extractor_get_method': 'get_teams'
    }
]


for context_item in context:
    lambda_dir = f"terraform/lambdas/{context_item['lambda_name']}"
    os.makedirs(lambda_dir, exist_ok=True)

    
    shutil.copytree("config", os.path.join(lambda_dir, "config"), dirs_exist_ok=True)

   
    shutil.copytree("scripts/utils", os.path.join(lambda_dir, "scripts/utils"), dirs_exist_ok=True)
    shutil.copytree("scripts/load", os.path.join(lambda_dir, "scripts/load"), dirs_exist_ok=True)

    
    os.makedirs(os.path.join(lambda_dir, "scripts/extract"), exist_ok=True)
    extractor_file = f"scripts/extract/{context_item['extractor_file_name']}.py"
    shutil.copy2(extractor_file, os.path.join(lambda_dir, "scripts/extract"))

    shutil.copy2("scripts/extract/base_extractor.py", os.path.join(lambda_dir, "scripts/extract"))
    
    shutil.copy2(".env", lambda_dir)

    
    rendered_code = template.render(context_item)
    template_filename = os.path.join(lambda_dir, f"lambda_function.py")
    with open(template_filename, 'w') as f:
        f.write(rendered_code)

    
    zip_path = os.path.join(lambda_dir, "payload_files.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(lambda_dir):
            for file in files:
                if file != "payload_files.zip":
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, lambda_dir)
                    zipf.write(file_path, arcname)

    print(f"Payload zip criado em '{zip_path}'")

    # Remove all files and folders except the .zip
    for item in os.listdir(lambda_dir):
        item_path = os.path.join(lambda_dir, item)
        if item != "payload_files.zip":
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)