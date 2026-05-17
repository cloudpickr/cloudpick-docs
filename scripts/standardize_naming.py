import os

files_to_process = [
    'CONTRIBUTING.md', 'README.md', 'about-cloud/accounts-and-organizations.md',
    'about-cloud/compare-clouds.md', 'about-cloud/console-cli-sdk.md',
    'about-cloud/decision-framework.md', 'about-cloud/getting-started.md',
    'about-cloud/iam-overview.md', 'about-cloud/pricing-model.md',
    'about-cloud/regions-and-zones.md', 'about-cloud/shared-responsibility.md',
    'about-cloud/support-plans.md', 'about-cloud/well-architected.md',
    'about-cloud/why-multicloud.md', 'ai/ai-ml.md', 'ai/embedding-models.md',
    'ai/generative-models.md', 'ai/getting-started.md', 'ai/llmops.md',
    'ai/multicloud-ai.md', 'ai/prompt-engineering.md', 'ai/rag-patterns.md',
    'compute/containers.md', 'compute/hybrid-and-edge.md', 'compute/virtual-machines.md',
    'database/managed-rdb.md', 'database/nosql.md', 'database/search.md',
    'devops/cicd.md', 'devops/devsecops.md', 'devops/iac.md', 'devops/monitoring.md',
    'devops/observability.md', 'devops/platform-engineering.md', 'devops/remote-access.md',
    'governance/compliance.md', 'governance/dr.md', 'governance/exit-strategy.md',
    'governance/finops.md', 'governance/landing-zone.md', 'networking/api-gateway.md',
    'networking/cdn.md', 'networking/dns.md', 'networking/load-balancer.md',
    'networking/multicloud-networking.md', 'networking/vpc-subnet.md',
    'security/ai-security.md', 'security/data-protection.md', 'security/iam.md',
    'security/network-isolation.md', 'security/security-posture.md', 'security/zero-trust.md',
    'storage/object-storage.md', 'GLOSSARY.md'
]

def process_file(file_path):
    if not os.path.exists(file_path):
        return
    
    content = None
    encodings = ['utf-8', 'utf-8-sig', 'cp949', 'latin-1']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
            
    if content is None:
        print(f"Could not decode {file_path}")
        return

    # Replace Google Cloud Platform first
    new_content = content.replace('Google Cloud Platform', 'Google Cloud')
    # Replace GCP
    new_content = new_content.replace('GCP', 'Google Cloud')
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

for f in files_to_process:
    process_file(f)
