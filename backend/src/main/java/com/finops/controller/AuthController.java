package com.finops.controller;

import com.finops.model.User;
import com.finops.service.UserService;
import com.finops.util.JwtUtil;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    @Resource
    private UserService userService;

    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody Map<String, String> loginInfo) {
        String username = loginInfo.get("username");
        String password = loginInfo.get("password");

        User user = userService.login(username, password);
        if (user == null) {
            Map<String, Object> error = new HashMap<>();
            error.put("code", 401);
            error.put("message", "用户名或密码错误");
            return error;
        }

        String token = JwtUtil.generateToken(user.getId(), user.getUsername(), user.getRole());

        Map<String, Object> result = new HashMap<>();
        result.put("code", 200);
        result.put("data", Map.of(
                "token", token,
                "user", Map.of(
                        "id", user.getId(),
                        "username", user.getUsername(),
                        "name", user.getName(),
                        "role", user.getRole(),
                        "departmentId", user.getDepartmentId()
                )
        ));

        return result;
    }

}
