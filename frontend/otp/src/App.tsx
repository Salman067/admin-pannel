import { BrowserRouter, Routes, Route } from "react-router-dom";
import SignUp from "../src/pages/SignUp";
import VerifyOTP from "../src/pages/VerifyOTP";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SignUp />} />
        <Route path="/verify_otp/:userId" element={<VerifyOTP />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
