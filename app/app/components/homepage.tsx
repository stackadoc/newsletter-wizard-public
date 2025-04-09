import React from 'react';
import { Button } from "~/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "~/components/ui/card";
import {Rocket, Rss, BrainCircuit, Send} from 'lucide-react';

export default function Homepage() {
    return (
        <div className="flex flex-col">
            <main className="flex-1">
                {/* Hero Section */}
                <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
                    <div className="container px-4 md:px-6 mx-auto">
                        <div className="flex flex-col items-center space-y-4 text-center">
                            <div className="space-y-2">
                                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none animate-in fade-in slide-in-from-bottom duration-700">
                                    Your AI-Powered Tech Digest
                                </h1>
                                <p className="mx-auto max-w-[700px] text-neutral-700 dark:invert md:text-xl animate-in fade-in slide-in-from-bottom duration-700 delay-150">
                                    Stay ahead of the curve. We curate the latest from Reddit, Discord, HackerNews, and more, synthesized by AI into a concise newsletter.
                                </p>
                            </div>
                            <div className="space-x-4 animate-in fade-in slide-in-from-bottom duration-700 delay-300">

                                <Button variant="outline" effect="expandIcon" icon={Rss} iconPlacement="right">
                                    Read Last News
                                </Button>

                                <Button effect="expandIcon" icon={Send} iconPlacement="right">
                                    Subscribe
                                </Button>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Use Cases Section */}
                <section className="w-full py-12 md:py-24 lg:py-32">
                    <div className="container px-4 md:px-6 mx-auto">
                        <h2 className="text-3xl font-bold tracking-tighter text-center sm:text-4xl md:text-5xl mb-12">
                            How It Works
                        </h2>
                        <div className="grid gap-6 md:grid-cols-3 lg:gap-12">
                            <Card className="transform transition-transform duration-300 hover:scale-105 hover:shadow-lg bg-white dark:bg-black border dark:border-neutral-700">
                                <CardHeader className="flex flex-col items-center text-center">
                                    <Rss className="w-12 h-12 mb-4" />
                                    <CardTitle>Information Gathering</CardTitle>
                                </CardHeader>
                                <CardContent className="text-center text-neutral-700 dark:invert">
                                    <p>We constantly scan top tech communities and news sources for the most relevant discussions and breakthroughs.</p>
                                </CardContent>
                            </Card>
                            <Card className="transform transition-transform duration-300 hover:scale-105 hover:shadow-lg bg-white dark:bg-black border dark:border-neutral-700">
                                <CardHeader className="flex flex-col items-center text-center">
                                    <BrainCircuit className="w-12 h-12 mb-4 " />
                                    <CardTitle>AI Synthesis</CardTitle>
                                </CardHeader>
                                <CardContent className="text-center text-neutral-700 dark:invert">
                                    <p>Our advanced LLM processes the collected data, identifying key themes and summarizing the core information.</p>
                                </CardContent>
                            </Card>
                            <Card className="transform transition-transform duration-300 hover:scale-105 hover:shadow-lg bg-white dark:bg-black border dark:border-neutral-700">
                                <CardHeader className="flex flex-col items-center text-center">
                                    <Rocket className="w-12 h-12 mb-4 " />
                                    <CardTitle>Newsletter Delivery</CardTitle>
                                </CardHeader>
                                <CardContent className="text-center text-neutral-700 dark:invert">
                                    <p>Receive a curated, easy-to-read newsletter directly in your inbox, saving you hours of research.</p>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </section>

            </main>
        </div>
    );
}