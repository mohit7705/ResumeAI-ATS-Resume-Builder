import { BrowserRouter } from "react-router-dom";
import { AppProvider } from "./context/AppContext";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <Dashboard />
      </AppProvider>
    </BrowserRouter>
  );
}

export default App;


