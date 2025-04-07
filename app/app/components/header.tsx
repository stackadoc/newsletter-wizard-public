import {ModeToggle} from "~/components/mode-toggle";
import {Button} from "~/components/ui/button";
import {Link} from "react-router";

const Header = () => {
    return (
        <header className="border-b sticky top-0 bg-background z-10 w-[100vw]">
            <nav className="flex items-center justify-between h-16 px-4 md:px-6 w-full">
                <div className="flex items-center gap-4">
                    <Link to="/">
                        <img
                            src="/logo.svg"
                            alt="App Logo"
                            width="24"
                            height="24"
                            className='dark:invert'
                        />
                    </Link>
                    <Link to="/">
                        <span className="font-semibold text-lg">My Awesome Blog</span>
                    </Link>
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm">Fake Button 1</Button>
                    <Button variant="ghost" size="sm">Fake Button 2</Button>
                    <Button variant="ghost" size="sm">Fake Button 3</Button>
                    <ModeToggle />
                </div>
            </nav>
        </header>
    )
}

export default Header;