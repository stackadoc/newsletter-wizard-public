import { Button } from "~/components/ui/button";
import { ArrowLeft } from "lucide-react";
import {useNavigate} from "react-router";

export default function BackButton() {
    const navigate = useNavigate();

    const goBack = () => {
        console.log("navigate =", navigate)
        // Prefer router's navigation if available, otherwise use browser history
        if (navigate) {
            navigate(-1); // Go back one step in the router's history
        } else {
            window.history.back(); // Fallback to browser history
        }
    };

    return (
        <Button variant="outline" size="sm" onClick={goBack}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
        </Button>
    );
}