<template>
	<div>
		<vue-particles
                class="login-background"
                color="#29ffc6"
                :particleOpacity="0.7"
                :particlesNumber="80"
                shapeType="circle"
                :particleSize="4"
                linesColor="#0cebeb"
                :linesWidth="1"
                :lineLinked="true"
                :lineOpacity="0.4"
                :linesDistance="150"
                :moveSpeed="3"
                :hoverEffect="true"
                hoverMode="grab"
                :clickEffect="true"
                clickMode="push">
        </vue-particles>
        <div class="login-win">
			<div class="login-body">
				<div class="login-title">
					抗疫物资管理系统
				</div>
				<div class="login-form">
					<el-form :model="loginForm" :rules="rules" ref="loginForm">
						<el-form-item style="margin-bottom:30px" prop="userName">
							<el-input type="text" 
                                v-model="loginForm.userName" suffix-icon="el-icon-user-solid"
                                placeholder="请输入您的账号"></el-input>
						</el-form-item>
						<el-form-item prop="passWord">
							<el-input type="password" 
                                v-model="loginForm.passWord" suffix-icon="el-icon-lock"
                                placeholder="请输入您的密码"></el-input>
						</el-form-item>
						<el-form-item>
							<el-button 
                                style="margin-top: 25px; width: 100%;background-color: #1CD8D2;"
                                @click="submitForm('loginForm')" 
                                type="primary">用户登录</el-button>
						</el-form-item>
					</el-form>
				</div>
			</div>
        </div>
    </div> 
</template>

<style>
	.login-background {
        background: linear-gradient(to right, #77a1d3, #79cbca, #e684ae);
        width: 100%;
        height: 100%; 
        z-index: -1;
        position: absolute;
    }
    .login-win {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 400px;
		height: 300px;
		padding: 15px 25px;
		border-radius: 5px;
        background-color: linear-gradient(to right, #77a1d3, #79cbca, #e684ae);
	}
	.login-body {
		
         width: 100%;
    }
	.login-title {
		text-align: center;
		font-size: 40px;
		font-weight: bold;
		color: #536976;
		margin-bottom: 45px;
		margin-top: 15px;
	}
</style>

<script>
	import initMenu from "../utils/menus.js";
	import { login } from '../api/index.js'

    export default {
        data(){

            return {
				loginForm: {
					userName: '',
					passWord: ''
				},
                rules: {
					userName: [{
						required: true,
						message: '用户账号必须输入',
						trigger: 'blur'
					}],
					passWord: [{
						required: true,
						message: '用户密码必须输入',
						trigger: 'blur'
					}],
				}
            }
            
        },
		methods: {
            
            submitForm(formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						
						login(this.loginForm).then(res => {
							
							this.$store.commit('setToken', res.data.token);
							sessionStorage.setItem("token", res.data.token);
							initMenu(this.$router, this.$store);
							this.$router.push('/index');
						});
                        
					} else {
						
						return false;
					}
				});
			}
        }
    }
</script>
