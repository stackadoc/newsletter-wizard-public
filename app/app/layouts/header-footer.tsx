import { Outlet } from "react-router";
import Header from "~/components/header";
import Footer from "~/components/footer";

export default function HeaderFooter() {
    return (
        <div className="flex flex-col min-h-screen">
            <Header />

            <div className="flex-1 flex flex-col items-center gap-16 pt-16 pb-4">
                <Outlet />
            </div>

            <Footer />
        </div>

    );
}
