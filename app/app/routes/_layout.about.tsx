import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "~/components/ui/avatar";
import { BrainCircuit, Rocket, Rss, Linkedin } from "lucide-react"; // Import Linkedin icon

export function meta() {
    return [
        { title: "About - Newsletter Wizard" },
        { name: "description", content: "Learn more about Newsletter Wizard and the team." },
    ];
}

export default function AboutPage() {
    // Placeholder team data with LinkedIn URLs
    const teamMembers = [
        {
            name: "Arthur RENAUD",
            title: "CEO",
            initials: "AR",
            imgSrc: "/profile-arthur-renaud.webp",
            linkedinUrl: "https://www.linkedin.com/in/arthur-renaud-a9993a49/",
        },
        {
            name: "Paul CHAUMEIL",
            title: "CTO",
            initials: "PC",
            imgSrc: "/profile-paul-chaumeil.webp",
            linkedinUrl: "https://www.linkedin.com/in/paul-chaumeil/",
        },
        {
            name: "Amin SAFFAR",
            title: "Lead Developer",
            initials: "AS",
            imgSrc: "/profile-amin-saffar.webp",
            linkedinUrl: "https://www.linkedin.com/in/aminsaffar/",
        },
    ];

    return (
        <div className="flex flex-col min-h-screen">
            <main className="flex-1 container mx-auto px-4 md:px-6 py-12">
                {/* Hero Section */}
                <section className="w-full mb-12 md:mb-24">
                    <div className="flex flex-col items-center space-y-4 text-center">
                        <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                            About Newsletter Wizard
                        </h1>
                        <p className="mx-auto max-w-[700px] text-neutral-700 dark:invert md:text-xl">
                            Newsletter Wizard is your personal AI assistant designed to keep you informed about the latest trends and discussions in the tech world. We simplify information discovery by curating content from diverse sources and delivering concise summaries directly to you.
                        </p>
                    </div>
                </section>

                {/* How It Works Section */}
                <section className="w-full my-12 md:my-24">
                    <h2 className="text-3xl font-bold tracking-tighter text-center sm:text-4xl md:text-5xl mb-12">
                        Our Process
                    </h2>
                    <div className="grid gap-6 md:grid-cols-3 lg:gap-12">
                        <Card className="bg-white dark:bg-black border dark:border-neutral-700">
                            <CardHeader className="flex flex-col items-center text-center">
                                <Rss className="w-12 h-12 mb-4" />
                                <CardTitle>Information Gathering</CardTitle>
                            </CardHeader>
                            <CardContent className="text-center text-neutral-700 dark:invert">
                                <p>We constantly scan top tech communities like Reddit, Discord, HackerNews, and various news sources for the most relevant discussions and breakthroughs.</p>
                            </CardContent>
                        </Card>
                        <Card className="bg-white dark:bg-black border dark:border-neutral-700">
                            <CardHeader className="flex flex-col items-center text-center">
                                <BrainCircuit className="w-12 h-12 mb-4" />
                                <CardTitle>AI Synthesis</CardTitle>
                            </CardHeader>
                            <CardContent className="text-center text-neutral-700 dark:invert">
                                <p>Our advanced Large Language Model (LLM) processes the collected data, identifying key themes, filtering noise, and summarizing the core information concisely.</p>
                            </CardContent>
                        </Card>
                        <Card className="bg-white dark:bg-black border dark:border-neutral-700">
                            <CardHeader className="flex flex-col items-center text-center">
                                <Rocket className="w-12 h-12 mb-4" />
                                <CardTitle>Newsletter Delivery</CardTitle>
                            </CardHeader>
                            <CardContent className="text-center text-neutral-700 dark:invert">
                                <p>You receive a curated, easy-to-read newsletter summarizing the findings, saving you valuable time and effort in staying updated.</p>
                            </CardContent>
                        </Card>
                    </div>
                </section>

                {/* Our Mission Section */}
                <section className="w-full my-12 md:my-24 text-center">
                    <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl mb-6">
                        Our Mission
                    </h2>
                    <p className="mx-auto max-w-[700px] text-neutral-700 dark:invert md:text-xl">
                        Our mission is to empower individuals and teams by providing timely, relevant, and synthesized information from the tech landscape, enabling them to stay ahead and make informed decisions without information overload.
                    </p>
                </section>

                {/* Team Section */}
                <section className="w-full my-12 md:my-24">
                    <h2 className="text-3xl font-bold tracking-tighter text-center sm:text-4xl md:text-5xl mb-12">
                        Meet the Team
                    </h2>
                    <div className="grid gap-8 md:grid-cols-3 lg:gap-12 justify-items-center">
                        {teamMembers.map((member) => (
                            <div key={member.name} className="flex flex-col items-center text-center">
                                <Avatar className="w-24 h-24 mb-4">
                                    <AvatarImage src={member.imgSrc} alt={member.name} className="object-cover saturate-[0.5]" />
                                    <AvatarFallback>{member.initials}</AvatarFallback>
                                </Avatar>
                                <h3 className="text-xl font-semibold">{member.name}</h3>
                                <p className="text-neutral-600 dark:invert mb-2">{member.title}</p>
                                {/* LinkedIn Link */}
                                <a
                                    href={member.linkedinUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
                                    aria-label={`${member.name}'s LinkedIn Profile`}
                                >
                                    <img
                                        src="/linkedin-icon.svg"
                                        alt="Linkedin"
                                        width="16"
                                        height="16"
                                        className='dark:invert'
                                    />
                                </a>
                            </div>
                        ))}
                    </div>
                </section>

            </main>
        </div>
    );
}