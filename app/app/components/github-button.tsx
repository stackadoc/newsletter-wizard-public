import React from 'react';
import { Button } from "~/components/ui/button";

export default function GithubRepoButton() {
    const repoUrl = "https://github.com/stackadoc/newsletter-wizard-public";

    return (
        <Button asChild variant="outline">
            <a href={repoUrl} target="_blank" rel="noopener noreferrer">
                <img
                    src="/github-icon.svg"
                    alt="GitHub Icon"
                    className="h-4 w-4 mr-2 dark:invert"
                />
                GitHub
            </a>
        </Button>
    );
}