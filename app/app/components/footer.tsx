import {Link} from "react-router";

const Footer = () => {
    return (
        <footer className="border-t">
            <div className="flex items-center justify-center h-16 px-4 md:px-6 text-sm text-muted-foreground">
                © {new Date().getFullYear()} Newsletter Wizard By&nbsp;
                <Link to="https://www.stackadoc.com" target="_blank">Stackadoc</Link>
                . All rights reserved.
            </div>
        </footer>
    )
}

export default Footer;