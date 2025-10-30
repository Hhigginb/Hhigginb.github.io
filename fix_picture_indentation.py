import re
from datetime import datetime

def fix_picture_indentation(file_path):
    """Fix indentation within picture tags - source, img, and closing tag should align properly"""
    
    # Create backup
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Save backup
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Backup saved: {backup_path}")
    
    lines = content.split('\n')
    fixed_lines = []
    changes_made = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is an opening picture tag (not a closing one)
        if '<picture>' in line and '</picture>' not in line:
            # Get the indentation of the opening picture tag
            picture_indent = len(line) - len(line.lstrip())
            fixed_lines.append(line)
            print(f"\nLine {i+1}: Found <picture> at indent {picture_indent}")
            i += 1
            
            # Process lines inside the picture tag until we find the closing tag
            while i < len(lines):
                inner_line = lines[i]
                
                # If we find the closing picture tag
                if '</picture>' in inner_line:
                    current_indent = len(inner_line) - len(inner_line.lstrip())
                    if current_indent != picture_indent:
                        # Fix the indentation to match opening tag
                        fixed_line = ' ' * picture_indent + inner_line.lstrip()
                        fixed_lines.append(fixed_line)
                        changes_made += 1
                        print(f"  Line {i+1}: Fixed </picture> indent from {current_indent} to {picture_indent}")
                    else:
                        fixed_lines.append(inner_line)
                    i += 1
                    break
                
                # If it's a source or img tag, it should be indented 2 spaces more than picture
                elif '<source' in inner_line or '<img' in inner_line:
                    current_indent = len(inner_line) - len(inner_line.lstrip())
                    expected_indent = picture_indent + 2
                    
                    if current_indent != expected_indent:
                        # Fix the indentation
                        fixed_line = ' ' * expected_indent + inner_line.lstrip()
                        fixed_lines.append(fixed_line)
                        changes_made += 1
                        tag_name = 'source' if '<source' in inner_line else 'img'
                        print(f"  Line {i+1}: Fixed <{tag_name}> indent from {current_indent} to {expected_indent}")
                    else:
                        fixed_lines.append(inner_line)
                    i += 1
                else:
                    # Keep other lines as-is
                    fixed_lines.append(inner_line)
                    i += 1
        else:
            # Not a picture tag, keep as-is
            fixed_lines.append(line)
            i += 1
    
    # Write the fixed content
    fixed_content = '\n'.join(fixed_lines)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"\nFixed {changes_made} indentation issues")
    return changes_made

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'hand.html'
    
    changes = fix_picture_indentation(file_path)
    print(f"\nTotal changes: {changes}")
