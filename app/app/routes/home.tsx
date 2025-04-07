import type { Route } from "./+types/home";
import { Welcome } from "~/welcome/welcome";
import HomePage from "~/components/homepage";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Newsletter Wizard" },
    { name: "description", content: "Welcome to Newsletter Wizard!" },
  ];
}

export default function Home() {
  return <HomePage />;
}
