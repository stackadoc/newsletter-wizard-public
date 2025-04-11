import {Send} from "lucide-react";
import {Button} from "~/components/ui/button";
import React from "react";
import {featureNotAvailableToast} from "~/lib/utils";

export default function SubscribeButton() {
    const onClick = () => {
        featureNotAvailableToast()
    }
    return (
        <Button
            effect="expandIcon"
            icon={Send}
            iconPlacement="right"
            onClick={onClick}
        >
            Subscribe
        </Button>
    )
}