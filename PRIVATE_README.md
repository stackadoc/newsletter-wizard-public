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
   # Add the public repository as a remote
   git remote add public https://github.com/your-username/newsletter-wizard-public.git
   
   # Push changes to the public repository
   git push public public-version:main
   ```

4. **Important Notes**
   - Always ensure sensitive data is removed before pushing to the public repository
   - The workflow file should have its schedule commented out in the public repository
   - Environment variables should be managed through GitHub Secrets, not in the code