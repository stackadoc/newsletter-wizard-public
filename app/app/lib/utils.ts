import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import {marked} from "marked";
import DOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const markdownToHtml = (markdown: string) => {
  const html = marked.parse(markdown) as string;
  const window = new JSDOM('').window;
  const purify = DOMPurify(window);
  return purify.sanitize(html);
}