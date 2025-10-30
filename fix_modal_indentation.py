import re
import sys
import os
from datetime import datetime

def fix_modal_indentation(file_path):
    """Fix indentation of source and img tags within picture elements in modals"""
    
    # Create backup
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Save backup
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Backup saved: {backup_path}")
        
        lines = content.split('\n')
        fixed_lines = []
        changes_made = 0
        in_picture = False
        picture_indent = 0
        
        for i, line in enumerate(lines):
            # Detect opening picture tag and record its indentation
            if '<picture>' in line and '</picture>' not in line:
                in_picture = True
                picture_indent = len(line) - len(line.lstrip())
                fixed_lines.append(line)
                continue
            
            # Fix indentation for tags inside picture element
            if in_picture:
                # Handle closing picture tag
                if '</picture>' in line:
                    in_picture = False
                    # Fix closing tag indentation to match opening tag
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent != picture_indent:
                        line = ' ' * picture_indent + line.lstrip()
                        changes_made += 1
                        print(f"Line {i+1}: Fixed </picture> indent from {current_indent} to {picture_indent}")
                
                # Handle source tags
                elif '<source srcset="responsive_images/' in line:
                    current_indent = len(line) - len(line.lstrip())
                    expected_indent = picture_indent + 2
                    if current_indent != expected_indent:
                        line = ' ' * expected_indent + line.lstrip()
                        changes_made += 1
                        print(f"Line {i+1}: Fixed <source> indent from {current_indent} to {expected_indent}")
                
                # Handle img tags
                elif '<img src="' in line:
                    current_indent = len(line) - len(line.lstrip())
                    expected_indent = picture_indent + 2
                    if current_indent != expected_indent:
                        line = ' ' * expected_indent + line.lstrip()
                        changes_made += 1
                        print(f"Line {i+1}: Fixed <img> indent from {current_indent} to {expected_indent}")
            
            fixed_lines.append(line)
        
        # Write fixed content
        fixed_content = '\n'.join(fixed_lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"\nFixed {changes_made} indentation issues in {file_path}")
        return changes_made
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        # Restore from backup if it exists
        if os.path.exists(backup_path):
            with open(backup_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Restored from backup due to error")
        return 0

if __name__ == '__main__':
    file_path = 'hand.html'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        sys.exit(1)
    
    changes = fix_modal_indentation(file_path)
    print(f"\nTotal changes: {changes}")
