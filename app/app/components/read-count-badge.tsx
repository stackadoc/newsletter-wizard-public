import { Badge } from "~/components/ui/badge";
import { Eye } from "lucide-react";

interface ReadCountBadgeProps {
    count: number;
}

/**
 * Formats a number into a shorter string with units (k for thousands).
 * e.g., 1234 -> 1.2k, 999 -> 999
 */
function formatReadCount(count: number): string {
    if (count >= 1000) {
        // Divide by 1000 and round to one decimal place
        const formatted = (count / 1000).toFixed(1);
        // Remove .0 if it exists (e.g., 1.0k -> 1k)
        return formatted.endsWith('.0') ? formatted.slice(0, -2) + 'k' : formatted + 'k';
    }
    return count.toString();
}

/**
 * Displays the number of reads with an icon, using shortened units for counts >= 1000.
 */
export function ReadCountBadge({ count }: ReadCountBadgeProps) {
    const displayCount = formatReadCount(count);

    return (
        <Badge variant="outline" className="flex items-center gap-1 text-xs text-muted-foreground">
            <Eye className="h-3 w-3" />
            {displayCount}
        </Badge>
    );
}