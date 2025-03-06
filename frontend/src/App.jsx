import "./App.css";
import { SessionProvider } from "./context/summaryContext";
import MainRoutes from "./routes/MainRoutes";

const App = () => {
  return (
    <div className="App w-full h-full">
      <SessionProvider>
        <MainRoutes />
      </SessionProvider>
    </div>
  );
};
export default App;
