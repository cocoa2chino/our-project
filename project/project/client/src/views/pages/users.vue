<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				<strong>信息查询</strong>
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item >
						<el-input v-model="qryForm.userName"
							placeholder="输入用户账号…"
							autocomplete="off"></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.name"
							placeholder="输入用户姓名…"
							autocomplete="off"></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.phone"
							placeholder="输入联系电话…"
							autocomplete="off"></el-input>
					</el-form-item>
					<el-form-item>
						<el-button type="primary"
							icon="el-icon-search" @click="getPageLikeInfo()"></el-button>
					</el-form-item>
				</el-form>
			</div>
		</el-card>

        <el-card shadow="never">
			<div slot="header">
				<el-button type="primary" size="mini"
						icon="el-icon-plus" @click="showAddWin()"></el-button>
			</div>
			<div>
				<el-table v-loading="loading" 
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
						<el-table-column align="center" type="index"></el-table-column>
						<el-table-column align="center" prop="userName" label="用户账号"></el-table-column>
						<el-table-column align="center" prop="name" label="用户姓名"></el-table-column>
						<el-table-column align="center" prop="gender" label="用户性别"></el-table-column>
						<el-table-column align="center" prop="age" label="用户年龄"></el-table-column>
						<el-table-column align="center" prop="phone" label="联系电话"></el-table-column>
						<el-table-column align="center" prop="address" label="联系地址"></el-table-column>
						<el-table-column align="center" label="用户类型">
							<template slot-scope="scope">
								<el-tag v-if="scope.row.type == 0">系统管理员</el-tag>
								<el-tag v-if="scope.row.type == 1">普通用户</el-tag>
							</template>
						</el-table-column>
						<el-table-column align="center" label="操作处理">
							<template slot-scope="scope">
								<el-button v-if="scope.row.type == 0" icon="el-icon-edit" disabled
										type="primary" size="mini" @click="showUpdWin(scope.row)"></el-button>
								<el-button v-if="scope.row.type == 0" icon="el-icon-delete" disabled
									type="danger" size="mini" @click="delUserInfo(scope.row.id)"></el-button>
								<el-button v-if="scope.row.type == 1" icon="el-icon-edit"
										type="primary" size="mini" @click="showUpdWin(scope.row)"></el-button>
								<el-button v-if="scope.row.type == 1" icon="el-icon-delete"
									type="danger" size="mini" @click="delUserInfo(scope.row.id)"></el-button>
							</template>
						</el-table-column>
				</el-table>
				<el-pagination v-if="pageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
					@current-change="handleCurrentChange" :current-page="pageIndex" :page-sizes="[10, 20, 50]"
					:page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="totalInfo">
				</el-pagination>
			</div>
        </el-card>

        <el-dialog title="添加信息" width="800px" :visible.sync="showAddFlag">
			<el-form label-width="90px" :model="usersForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="用户账号">
							<el-input v-model="usersForm.userName" 
								placeholder="请输入用户账号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="用户密码">
							<el-input type="password" v-model="usersForm.passWord" 
								placeholder="请输入用户密码…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="用户姓名">
							<el-input v-model="usersForm.name" 
								placeholder="请输入用户姓名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="用户年龄">
							<el-input v-model="usersForm.age" 
								placeholder="请输入用户年龄…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="用户性别">
							<el-radio-group v-model="usersForm.gender">
								<el-radio label="男" value="男"></el-radio>
								<el-radio label="女" value="女"></el-radio>
							</el-radio-group>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="联系电话">
							<el-input  v-model="usersForm.phone" 
								placeholder="请输入联系电话…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="24">
						<el-form-item label="联系地址">
							<el-input type="textarea" v-model="usersForm.address" 
								:rows="4" placeholder="请输入联系地址…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showAddFlag = false">取 消</el-button>
				<el-button type="primary" @click="addUserInfo()">确 定</el-button>
			</div>
		</el-dialog>

        <el-dialog title="修改信息" width="800px" :visible.sync="showUpdFlag">
			<el-form label-width="90px" :model="usersForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="用户账号">
							<el-input v-model="usersForm.userName" 
								placeholder="请输入用户账号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="用户密码">
							<el-input type="password" v-model="usersForm.passWord" 
								placeholder="请输入用户密码…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="用户姓名">
							<el-input v-model="usersForm.name" 
								placeholder="请输入用户姓名…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="用户年龄">
							<el-input v-model="usersForm.age" 
								placeholder="请输入用户年龄…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="用户性别">
							<el-radio-group v-model="usersForm.gender">
								<el-radio label="男" value="男"></el-radio>
								<el-radio label="女" value="女"></el-radio>
							</el-radio-group>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="联系电话">
							<el-input  v-model="usersForm.phone" 
								placeholder="请输入联系电话…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="24">
						<el-form-item label="联系地址">
							<el-input type="textarea" v-model="usersForm.address" 
								:rows="4" placeholder="请输入联系地址…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showUpdFlag = false">取 消</el-button>
				<el-button type="primary" @click="updUserInfo()">确 定</el-button>
			</div>
		</el-dialog>
    </div>
</template>

<style>

</style>

<script>

	import { 
		getPageUsers,
		addUsers,
		updUsers,
		delUsers 
	} from '../../api/index.js'

    export default{

        data(){

            return {
                pageInfos: [],
				pageIndex: 1,
				pageSize: 10,
				pageTotal: 0,
				totalInfo: 0,
				loading: true,
				showAddFlag: false,
				showUpdFlag: false,
				usersForm: {
					id: "",
					userName: "",
					passWord: "",
					name: "",
					gender: "",
					age: "",
					phone: "",
					address: "",
					type: "",
				},
                qryForm: {
					userName: "",
					name: "",
					phone: "",
				},
            }
        },
        methods: {

            getPageInfo(pageIndex, pageSize) {

				getPageUsers(pageIndex, pageSize, this.qryForm.userName, 
								this.qryForm.name, this.qryForm.phone).then(resp => {

					this.pageInfos = resp.data.data;
					this.pageIndex = resp.data.pageIndex;
					this.pageSize = resp.data.pageSize;
					this.pageTotal = resp.data.pageTotal;
					this.totalInfo = resp.data.count;

					this.loading = false;
				});
			},
            getPageLikeInfo() {
				getPageUsers(1, this.pageSize, this.qryForm.userName, 
								this.qryForm.name, this.qryForm.phone).then(resp => {

					this.pageInfos = resp.data.data;
					this.pageIndex = resp.data.pageIndex;
					this.pageSize = resp.data.pageSize;
					this.totalInfo = resp.data.count;
					this.pageTotal = resp.data.pageTotal;
					this.loading = false;
				});
			},
			handleSizeChange(pageSize) {

				this.getPageInfo(this.pageIndex, pageSize, this.qryForm.userName, 
								this.qryForm.name, this.qryForm.phone);
			},
			handleCurrentChange(pageIndex) {

				this.getPageInfo(pageIndex, this.pageSize, this.qryForm.userName, 
								this.qryForm.name, this.qryForm.phone);
			},
			initUserForm() {

				this.usersForm = {
					id: "",
					userName: "",
					passWord: "",
					name: "",
					gender: "",
					age: "",
					phone: "",
					address: "",
					type: "1",
				}
			},
            showAddWin() {

				this.initUserForm();
				this.showAddFlag = true;
			},
			showUpdWin(row) {

				this.usersForm = row;
				
				this.showUpdFlag = true;
			},
			addUserInfo(){

				addUsers(this.usersForm).then(resp =>{

					this.$message({
						message: resp.msg,
						type: 'success'
					});
					
					this.getPageInfo(1, this.pageSize);

					this.showAddFlag = false;
				});
			},
			updUserInfo(){

				updUsers(this.usersForm).then(resp =>{

					this.$message({
						message: resp.msg,
						type: 'success'
					});

					this.getPageInfo(1, this.pageSize);

					this.showUpdFlag = false;
				});
			},
			delUserInfo(id){

				this.$confirm('即将删除相关信息, 是否继续?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(() => {
					
					delUsers(id).then(resp =>{
					
						this.$message({
							message: resp.msg,
							type: 'success'
						});

						this.getPageInfo(1, this.pageSize);
					});	
				});			
			}
        },
        mounted(){

			this.getPageInfo(1, this.pageSize);
        }
    }
</script>
