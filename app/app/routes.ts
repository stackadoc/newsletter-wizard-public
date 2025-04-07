import type { RouteConfig } from "@react-router/dev/routes";
import {
    index,
    layout,
} from "@react-router/dev/routes";

export default [
    layout("layouts/header-footer.tsx", [
        index("routes/home.tsx"),
    ]),
] satisfies RouteConfig;
