import { useCallback } from "react";
import { useAppDispatch, useAppSelector } from "@/redux/hooks";
import { clearAuth } from "@/redux/slices/authSlice";
import {
  loginUser,
  registerUser,
  logoutUser,
} from "@/redux/thunks/authThunks";
import type { LoginRequest, RegisterRequest } from "@/services/authService";

export const useAuth = () => {
  const dispatch = useAppDispatch();
  const { user, accessToken, isAuthenticated, isLoading, error } =
    useAppSelector((state) => state.auth);

  const login = useCallback(
    async (credentials: LoginRequest) => {
      const result = await dispatch(
        loginUser(credentials as { email: string; password: string })
      );
      if (loginUser.fulfilled.match(result)) {
        return result.payload;
      }
      throw new Error(result.payload as string);
    },
    [dispatch]
  );

  const register = useCallback(
    async (data: RegisterRequest) => {
      const result = await dispatch(registerUser(data));
      if (registerUser.fulfilled.match(result)) {
        return result.payload;
      }
      throw new Error(result.payload as string);
    },
    [dispatch]
  );

  const logout = useCallback(() => {
    dispatch(logoutUser()).then(() => {
      dispatch(clearAuth());
    });
  }, [dispatch]);

  return {
    user,
    accessToken,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
  };
};
