#!/usr/bin/env python3
import json
import os
import shutil
import uuid

def generate_boundary_data(tenant_code, tenant_name):
    """Generate boundary data structure for a tenant"""
    return {
        "tenantId": tenant_code,
        "moduleName": "egov-location",
        "TenantBoundary": [
            {
                "hierarchyType": {
                    "code": "REVENUE",
                    "name": "REVENUE"
                },
                "boundary": {
                    "id": 1,
                    "boundaryNum": 1,
                    "name": tenant_name,
                    "localname": tenant_name,
                    "longitude": None,
                    "latitude": None,
                    "label": "City",
                    "code": tenant_code,
                    "children": [
                        {
                            "id": str(uuid.uuid4()),
                            "boundaryNum": 1,
                            "name": "ZONE_1",
                            "localname": "ZONE_1",
                            "longitude": None,
                            "latitude": None,
                            "label": "Zone",
                            "code": "Z1",
                            "children": [
                                {
                                    "id": str(uuid.uuid4()),
                                    "boundaryNum": 1,
                                    "name": "WARD_1",
                                    "localname": "WARD_1",
                                    "longitude": None,
                                    "latitude": None,
                                    "label": "Block",
                                    "code": "W1",
                                    "children": [
                                        {
                                            "id": str(uuid.uuid4()),
                                            "boundaryNum": 1,
                                            "name": tenant_name,
                                            "localname": tenant_name,
                                            "longitude": None,
                                            "latitude": None,
                                            "label": "Locality",
                                            "code": "L1",
                                            "area": "Area1",
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }

def main():
    # Read tenants.json
    with open('data/pg/tenant/tenants.json', 'r', encoding='utf-8') as f:
        tenants_data = json.load(f)
    
    # Remove old directories with pg. prefix
    for tenant in tenants_data['tenants']:
        old_dir = f"data/{tenant['code']}"
        if os.path.exists(old_dir):
            shutil.rmtree(old_dir)
            print(f"Removed: {old_dir}")
    
    # Create new directories without pg. prefix
    for tenant in tenants_data['tenants']:
        tenant_code = tenant['code']
        tenant_name = tenant['name']
        
        # Remove pg. prefix from folder name
        folder_name = tenant_code.replace('pg.', '')
        
        # Create directory structure
        dir_path = f"data/{folder_name}/egov-location"
        os.makedirs(dir_path, exist_ok=True)
        
        # Generate boundary data
        boundary_data = generate_boundary_data(tenant_code, tenant_name)
        
        # Write boundary-data.json file
        file_path = f"{dir_path}/boundary-data.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(boundary_data, f, indent=2, ensure_ascii=False)
        
        print(f"Created: {file_path}")

if __name__ == "__main__":
    main()