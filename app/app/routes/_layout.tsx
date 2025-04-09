import { Outlet } from "react-router";
import Header from "~/components/header";
import Footer from "~/components/footer";

export default function HeaderFooter() {
    return (
        <div className="flex flex-col min-h-screen">
            <Header />

            <main className="flex-grow py-8 px-4 md:px-6" >
                <Outlet />
            </main>

            <Footer />
        </div>

    );
}
