import { useState } from "react";
import {
  Box,
  TextField,
  Button,
  Card,
  CardContent,
  CardHeader,
  IconButton,
  Grid,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const SignUpComponent: React.FC = () => {
  const navigate = useNavigate();





  const [newUser, setNewUser] = useState({
    phoneNumber: "",
    email: "",
    password1: "",
    password2: "",
  });

  const [showPassword1, setShowPassword1] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);

  const url = "http://127.0.0.1:8000/user/";

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setNewUser((prev) => ({ ...prev, [name]: value }));
  };

  const validatePhoneNumber = (value: string) => {
    return (
      value &&
      value.length === 11 &&
      /^[0-9]{11}$/.test(value) &&
      "Phone Number is valid"
    );
  };

  const handleReset = () => {
    setNewUser({ phoneNumber: "", email: "", password1: "", password2: "" });
  };

  const handleRegister = () => {
    const data = {
      phone_number: newUser.phoneNumber,
      email: newUser.email,
      password1: newUser.password1,
      password2: newUser.password2,
    };
  
    axios
      .post(url, data, {
        headers: {
          "Content-Type": "application/json", // Ensures the data is treated as JSON
        },
      })
      .then((response) => {
        console.log(response);
        const id = response.data.id;
        navigate(`/verify_otp/${id}`);
      })
      .catch((error) => {
        alert(error.response?.data.phone_number[0]);
        console.error("Error registering user:", error.response?.data.phone_number[0] || error.message);
      });
  };
  
  return (
    <Box mt={5} display="flex" justifyContent="center">
      <Grid container justifyContent="center">
        <Grid item xs={12} sm={8} md={4}>
          <Card>
            <CardHeader title="Register Form" />
            <CardContent>
              <Box mb={2}>
                <TextField
                  name="phoneNumber"
                  label="Phone Number"
                  value={newUser.phoneNumber}
                  onChange={handleChange}
                  fullWidth
                  required
                  inputProps={{ maxLength: 11 }}
                  error={!!newUser.phoneNumber && !validatePhoneNumber(newUser.phoneNumber)}
                  helperText={
                    !!newUser.phoneNumber &&
                    !validatePhoneNumber(newUser.phoneNumber) &&
                    "Phone Number must be 11 digits and only numbers"
                  }
                />
              </Box>
              <Box mb={2}>
                <TextField
                  name="email"
                  label="Email"
                  value={newUser.email}
                  onChange={handleChange}
                  fullWidth
                  required
                />
              </Box>
              <Box mb={2} position="relative">
                <TextField
                  name="password1"
                  label="Password"
                  type={showPassword1 ? "text" : "password"}
                  value={newUser.password1}
                  onChange={handleChange}
                  fullWidth
                  required
                  helperText="At least 8 characters"
                  InputProps={{
                    endAdornment: (
                      <IconButton
                        onClick={() => setShowPassword1(!showPassword1)}
                        edge="end"
                      >
                        {showPassword1 ? <Visibility /> : <VisibilityOff />}
                      </IconButton>
                    ),
                  }}
                />
              </Box>
              <Box mb={2} position="relative">
                <TextField
                  name="password2"
                  label="Repeat Password"
                  type={showPassword2 ? "text" : "password"}
                  value={newUser.password2}
                  onChange={handleChange}
                  fullWidth
                  required
                  helperText="At least 8 characters"
                  InputProps={{
                    endAdornment: (
                      <IconButton
                        onClick={() => setShowPassword2(!showPassword2)}
                        edge="end"
                      >
                        {showPassword2 ? <Visibility /> : <VisibilityOff />}
                      </IconButton>
                    ),
                  }}
                />
              </Box>
              <Box mt={3} display="flex" justifyContent="space-between">
                <Button variant="outlined" onClick={handleReset}>
                  Clear
                </Button>
                <Button
                  variant="contained"
                  color="success"
                  disabled={
                    !newUser.phoneNumber ||
                    !newUser.password1 ||
                    !newUser.password2
                  }
                  onClick={handleRegister}
                >
                  Register
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SignUpComponent;
