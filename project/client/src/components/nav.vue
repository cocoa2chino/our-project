<template>
  <el-header class="fater-header">
    
    <el-dropdown @command="handleUser" class="fater-header-user">   
        <el-avatar :size="40" :src="avatarUrl"></el-avatar>
        <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="info"><strong>个人信息</strong></el-dropdown-item>
            <el-dropdown-item command="pwd"><strong>修改密码</strong></el-dropdown-item>
            <el-dropdown-item command="exit"><strong>退出系统</strong></el-dropdown-item>
        </el-dropdown-menu>
    </el-dropdown>

    <el-dialog
      title="修改信息" width="600px"
      :append-to-body="true" :visible.sync="showUpdInfoFlag">
      <el-form label-width="80px" :model="userForm">
          <el-form-item label="用户账号">
              <el-input v-model="userForm.userName" 
                  placeholder="请输入用户账号…" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="用户姓名">
              <el-input v-model="userForm.name" 
                  placeholder="请输入用户姓名…" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="用户年龄">
              <el-input v-model="userForm.age" 
                  placeholder="请输入用户年龄…" autocomplete="off"></el-input>
          </el-form-item>  
          <el-form-item label="用户性别">
              <el-radio-group v-model="userForm.gender">
                  <el-radio label="男"></el-radio>
                  <el-radio label="女"></el-radio>
              </el-radio-group>
          </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
          <el-button @click="showUpdInfoFlag = false">取 消</el-button>
          <el-button type="primary" @click="updInfo()">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="修改密码" width="600px"
      :append-to-body="true" :visible.sync="showUpdPwdFlag">
      <el-form label-width="80px"  ref="userPwd" :model="userPwd" :rules="userPwdFormRules">
          <el-form-item label="原始密码" prop="oldPwd">
            <el-input
                type="password" v-model="userPwd.oldPwd"
                placeholder="请输入原始密码……" autocomplete="off"></el-input>
          </el-form-item>
        <el-form-item label="修改密码" prop="newPwd">
          <el-input
              type="password" v-model="userPwd.newPwd"
              placeholder="请输入修改密码……" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="rePwd">
          <el-input
            type="password" v-model="userPwd.rePwd"
            placeholder="请再次确认密码……" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
          <el-button @click="showUpdPwdFlag = false">取 消</el-button>
          <el-button type="primary" @click="updPwd('userPwd')">确 定</el-button>
      </div>
    </el-dialog>
  </el-header>
</template>

<style>
</style>

<script>
import {
  exit,
  getLoginUser,
  checkUserPwd,
  updLoginUserInfo,
  updLoginUserPwd,
} from "../api";

import avatarUrl from '../assets/avatar.png'

export default {
  data() {
    var checkOldPwd = async (rule, value, callback) => {
      if (value) {
        await checkUserPwd(this.$store.state.token, value).then((resp) => {
          if(resp.code != 0){
             callback(new Error(resp.msg));
          }
        });
      } else {
        callback(new Error("原始密码必须输入"));
      }
      callback();
    };
    var checkNewPwd = (rule, value, callback) => {
      if (!value) {
        callback(new Error("修改密码必须输入"));
      }

      callback();
    };
    var checkRePwd = (rule, value, callback) => {
      if (!value) {
        callback(new Error("确认密码必须输入"));
      }

      if (value != this.userPwd.newPwd) {
        callback(new Error("两次输入密码不一致"));
      }

      callback();
    };
    return {
      showUpdInfoFlag: false,
      showUpdPwdFlag: false,
      userPwd: {
        oldPwd: "",
        newPwd: "",
        rePwd: "",
      },
      userPwdFormRules: {
        oldPwd: [
          {
            validator: checkOldPwd,
            trigger: "blur",
          },
        ],
        newPwd: [
          {
            validator: checkNewPwd,
            trigger: "blur",
          },
        ],
        rePwd: [
          {
            validator: checkRePwd,
            trigger: "blur",
          },
        ],
      },
      userForm: {
        id: "",
        userName: "",
        passWord: "",
        name: "",
        gender: "",
        age: "",
        phone: "",
      },
      avatarUrl: avatarUrl
    };
  },
  methods: {
    handleUser(comm) {
      if (comm == "info") {
        this.showUpdInfoWin();
      }

      if (comm == "pwd") {
        this.showUpdPwdWin();
      }

      if (comm == "exit") {
        this.$confirm("确认要退出吗？", "系统提示", {
          confirmButtonText: "确认",
          cancelButtonText: "取消",
          type: "warning",
        }).then(() => {
          exit(this.$store.state.token).then(() => {
            this.$store.commit("clearToken");
            this.$store.commit("clearMenus");
            sessionStorage.clear();
            this.$router.push("/");
          });
        });
      }
    },
    initUserPwd() {
      this.userPwd = {
        oldPwd: "",
        newPwd: "",
        rePwd: "",
      };
    },
    initUserForm() {
      this.userForm = {
        id: "",
        userName: "",
        passWord: "",
        name: "",
        gender: "",
        age: "",
        phone: "",
        token: this.$store.state.token
      };
    },
    showUpdInfoWin() {
      getLoginUser(this.$store.state.token).then((resp) => {
        this.initUserForm();
        this.userForm = resp.data;
        this.showUpdInfoFlag = true;
      });
    },
    showUpdPwdWin() {
      this.initUserPwd();
      this.showUpdPwdFlag = true;
    },
    updInfo() {
		

		this.userForm.token = this.$store.state.token;
      updLoginUserInfo(this.userForm).then((resp) => {
        this.$message({
          message: resp.msg,
          type: "success",
        });

        this.showUpdInfoFlag = false;
        this.initUserForm();
      });
    },
    updPwd(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          updLoginUserPwd(this.$store.state.token, this.userPwd.newPwd).then((resp) => {
            this.$message({
              message: resp.msg,
              type: "success",
            });

            this.showUpdPwdFlag = false;
            this.initUserPwd();
          });
        } else {
          return false;
        }
      });
    },
  },
};
</script>