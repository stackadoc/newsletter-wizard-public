### Managing Private and Public Repositories

This project uses a private repository for development and a public repository for sharing. Here's how to manage them:

1. **Private Repository (Development)**
   - Contains the actual workflow with the schedule uncommented
   - Stores all sensitive environment variables in GitHub Secrets
   - Used for actual newsletter generation

2. **Public Repository (Sharing)**
   - Fork of the private repository
   - Workflow schedule is commented out by default
   - Serves as a template for others to use

3. **Pushing Changes from Private to Public**
   ```bash
   # Add the public repository as a remote (do it only once)
   git remote add public git@github.com:stackadoc/newsletter-wizard-public.git
   
   # Switch to public branch
   git checkout public-version

   # Update the public branch
   git merge origin/main

   # Push the updates
   git push

   # Push to public repository
   git push public public-version:main
   ```

4. **Important Notes**
   - Always ensure sensitive data is removed before pushing to the public repository
   - The workflow file should have its schedule commented out in the public repository
   - Environment variables should be managed through GitHub Secrets, not in the code