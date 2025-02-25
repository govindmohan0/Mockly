import { useLocation, useRoutes } from "react-router-dom";
import Login from "./components/auth/login";
import Register from "./components/auth/register";
import Header from "./components/header";
import Home from "./components/home";
import Videocallon from "./components/pages/Videocallon";
import { AuthProvider } from "./contexts/authContext";

function App() {
  const location = useLocation(); // Get current route
  const hideHeaderRoutes = ["/interview"]; // Paths where header should be hidden

  const routesArray = [
    { path: "*", element: <Login /> },
    { path: "/login", element: <Login /> },
    { path: "/register", element: <Register /> },
    { path: "/home", element: <Home /> },
    { path: "/interview", element: <Videocallon /> },
  ];

  let routesElement = useRoutes(routesArray);

  return (
    <AuthProvider>
      {/* Conditionally render Header */}
      {!hideHeaderRoutes.includes(location.pathname) && <Header />}
      
      <div className="w-full h-screen flex flex-col">
        {routesElement}
      </div>
    </AuthProvider>
  );
}

export default App;
