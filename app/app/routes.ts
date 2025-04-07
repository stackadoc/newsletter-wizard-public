import {route, type RouteConfig} from "@react-router/dev/routes";
import {
    index,
    layout,
} from "@react-router/dev/routes";

export default [
    layout("layouts/header-footer.tsx", [
        index("routes/home.tsx"),
    ]),
    route("action/set-theme", "routes/action.set-theme.ts"),
] satisfies RouteConfig;
