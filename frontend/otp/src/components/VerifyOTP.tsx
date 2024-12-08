import { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  TextField,
  Grid,
} from "@mui/material";
import axios, { AxiosError } from "axios";

interface OTPVerificationProps {
  userId: string;
}

const OTPVerification: React.FC<OTPVerificationProps> = ({ userId }) => {
  const [otp, setOtp] = useState<string>("");
  const [error, setError] = useState<string>("");
  const url = "http://127.0.0.1:8000/user/";

  const regenerateOtp = async () => {
    const regenerateUrl = `${url}${userId}/regenerate_otp/`;
    try {
      const response = await axios.patch<{ message: string }>(regenerateUrl);
      alert(response.data.message);
    } catch (err) {
      const axiosError = err as AxiosError<{ message: string }>;
      console.error(axiosError.response?.data?.message || axiosError.message);
      alert(axiosError.response?.data?.message || "Error regenerating OTP");
    }
  };

  const verifyOtp = async () => {
    const verifyUrl = `${url}${userId}/verify_otp/`;
    const data = { otp };

    try {
      const response = await axios.patch<{ message: string }>(verifyUrl, data);
      console.log(response.data);
    } catch (err) {
      const axiosError = err as AxiosError<{ message: string }>;
      console.error(axiosError.response?.data?.message || axiosError.message);
      alert(axiosError.response?.data?.message || "Error verifying OTP");
      setOtp("");
    }
  };

  const validateOtp = (value: string): boolean => {
    if (!value) {
      setError("OTP is required");
      return false;
    } else if (value.length > 4) {
      setError("OTP must be less than 5 characters");
      return false;
    }
    setError("");
    return true;
  };

  const handleOtpChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (validateOtp(value)) {
      setOtp(value);
    } else {
      setOtp("");
    }
  };

  return (
    <Box mt={5} display="flex" justifyContent="center">
      <Grid container justifyContent="center">
        <Grid item xs={12} sm={8} md={4}>
          <Card>
            <CardHeader title="OTP Verification" className="text-center" />
            <CardContent>
              <TextField
                value={otp}
                onChange={handleOtpChange}
                label="OTP"
                variant="outlined"
                fullWidth
                required
                inputProps={{ maxLength: 4 }}
                helperText={error}
                error={!!error}
              />

              <Box mt={3} display="flex" justifyContent="space-between">
                <Button
                  color="secondary"
                  variant="outlined"
                  onClick={regenerateOtp}
                >
                  Regenerate OTP
                </Button>

                <Button
                  color="success"
                  variant="contained"
                  disabled={!otp || !!error}
                  onClick={verifyOtp}
                >
                  Verify OTP
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default OTPVerification;