import re
from datetime import datetime

def fix_modal_rack_classes(file_path):
    """Change mySlides class to mySlides3 in modal-rack section"""
    
    # Create backup
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Save backup
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Backup saved: {backup_path}")
    
    in_modal_rack = False
    changes_made = 0
    
    for i, line in enumerate(lines):
        # Detect start of modal-rack
        if 'id="modal-rack"' in line:
            in_modal_rack = True
            print(f"Line {i+1}: Found modal-rack start")
        
        # Detect end of modal-rack (start of next modal)
        if in_modal_rack and 'id="modal-uke"' in line:
            in_modal_rack = False
            print(f"Line {i+1}: Found modal-rack end")
        
        # Replace mySlides with mySlides3 in modal-rack section
        if in_modal_rack and 'class="mySlides' in line:
            old_line = line
            line = line.replace('class="mySlides ', 'class="mySlides3 ')
            if line != old_line:
                lines[i] = line
                changes_made += 1
                print(f"Line {i+1}: Changed mySlides to mySlides3")
    
    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\nFixed {changes_made} slide classes in modal-rack")
    return changes_made

if __name__ == '__main__':
    file_path = 'hand.html'
    changes = fix_modal_rack_classes(file_path)
    print(f"\nTotal changes: {changes}")
