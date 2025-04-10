import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import {marked} from "marked";
// import DOMPurify from 'dompurify';
// import { JSDOM } from 'jsdom';
import DOMPurify from 'isomorphic-dompurify';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const markdownToHtml = (markdown: string) => {
  // const html = marked.parse(markdown) as string;
  // const window = new JSDOM('').window;
  // const purify = DOMPurify(window);
  return DOMPurify.sanitize(marked.parse(markdown) as string);
}

// Function to add target="_blank" to links in an HTML string
export function addTargetBlankToLinks(htmlString: string): string {
  // This regex finds <a> tags and captures their existing attributes
  // It then checks if 'target=' is already present. If not, it adds target and rel.
  return htmlString.replace(/<a(\s+[^>]+)>/gi, (match, attributes) => {
    // Check if target attribute already exists in the captured attributes
    if (attributes && attributes.toLowerCase().includes('target=')) {
      // If target exists, return the original tag unchanged
      return match;
    } else {
      // If target doesn't exist, add target="_blank" and rel="noopener noreferrer"
      // Ensure attributes has a leading space if it exists
      const space = attributes && !attributes.startsWith(' ') ? ' ' : '';
      return `<a target="_blank" rel="noopener noreferrer"${space}${attributes || ''}>`;
    }
  });
}