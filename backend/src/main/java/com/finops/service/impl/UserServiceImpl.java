package com.finops.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.finops.mapper.UserMapper;
import com.finops.model.User;
import com.finops.service.UserService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    @Resource
    private PasswordEncoder passwordEncoder;

    @Override
    public User login(String username, String password) {
        User user = getByUsername(username);
        if (user != null && passwordEncoder.matches(password, user.getPassword())) {
            return user;
        }
        return null;
    }

    @Override
    public User getByUsername(String username) {
        return baseMapper.selectOne(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <User>lambdaQuery().eq(User::getUsername, username)
        );
    }

}
