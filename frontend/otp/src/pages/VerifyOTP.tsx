import { useParams, useNavigate } from "react-router-dom";
import VerifyOTPComponent from "../components/VerifyOTP";

const VerifyOTP: React.FC = () => {
  const { userId } = useParams<{ userId?: string }>(); // Use optional chaining
  const navigate = useNavigate();
  if (!userId) {
    navigate("/error"); 
    return null;
  }

  return <VerifyOTPComponent userId={userId} />;
};

export default VerifyOTP;
