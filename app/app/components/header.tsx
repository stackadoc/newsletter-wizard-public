import {ModeToggle} from "~/components/mode-toggle";

const Header = () => {
    return (
        <header>
            <div className="w-[100vw] p-4">
                Header
                <ModeToggle />
            </div>
        </header>
    )
}

export default Header;