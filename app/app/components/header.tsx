import {ModeToggle} from "~/components/mode-toggle";
import {Button} from "~/components/ui/button";
import {Link} from "react-router";

const Header = () => {
    return (
        <header className="border-b sticky top-0 bg-background z-10">
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
                        <span className="font-semibold text-lg">Newsletter Wizard</span>
                    </Link>
                </div>
                <div className="flex items-center gap-2">
                    <Link to="/newsletters">
                        <Button variant="ghost" size="sm">Newsletters</Button>
                    </Link>
                    <Link to="/about">
                        <Button variant="ghost" size="sm">About</Button>
                    </Link>
                    <ModeToggle />
                </div>
            </nav>
        </header>
    )
}

export default Header;