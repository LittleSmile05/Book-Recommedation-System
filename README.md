# Book-Recommedation-System

# 1. Define variables for clarity
REPO_URL="https://github.com/LittleSmile05/Book-Recommedation-System.git"
REPO_DIR="Book-Recommedation-System"
COMMIT_MSG="FEAT: Implemented dynamic HTML frontend with favorites and load more."

# 2. Clone the repository
echo "Cloning repository..."
git clone $REPO_URL

# 3. Copy your project files into the cloned directory
#    !! ASSUMPTION: This copies ALL files from your current directory (e.g., your updated index.html, app.py, etc.) 
#    !! into the newly cloned repo folder, overwriting existing files.
echo "Copying local files into the clone..."
cp -r ./* $REPO_DIR/
cp -r ./.??* $REPO_DIR/ 2>/dev/null  # For hidden files like .gitignore, ignoring errors if none exist

# 4. Navigate into the repository directory
cd $REPO_DIR

# 5. Stage all changes (new, modified, and deleted files)
echo "Adding and staging all changes..."
git add .

# 6. Commit the changes
echo "Committing with message: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# 7. Push the changes to the 'main' branch
echo "Pushing to GitHub..."
git push origin main

<img width="1888" height="882" alt="image" src="https://github.com/user-attachments/assets/14582a6b-dc25-42de-837c-030cde2f4c11" />
<img width="1892" height="894" alt="image" src="https://github.com/user-attachments/assets/7df06a8e-6adf-4b0b-98d3-d94f337fec37" />
<img width="1206" height="772" alt="image" src="https://github.com/user-attachments/assets/b7819540-cbba-4ff3-90f5-2a36d97ed78f" />


# 8. Clean up (optional: move back to the original directory)
cd ..
echo "Done. Changes pushed to the remote repository."
