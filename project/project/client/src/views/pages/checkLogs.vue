<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				<strong>信息查询</strong>
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item >
						<el-select v-model="qryForm.resl" placeholder="请选择入/出库类型">
							<el-option label="入库" value="入库"></el-option>
							<el-option label="出库" value="出库"></el-option>
						</el-select>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.loc"
							placeholder="输入物资名称…"
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
				<el-button v-if="userType == 0" icon="el-icon-plus" disabled
					type="primary" size="mini" @click="showAddWin()"></el-button>
				<el-button v-if="userType == 1" icon="el-icon-edit"
					type="primary" size="mini" @click="showAddWin()"></el-button>
			</div>
			<div>
				<el-table v-loading="loading" 
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
						<el-table-column align="center" type="index"></el-table-column>
						<el-table-column align="center" prop="createTime" label="入/出库时间"></el-table-column>
						<el-table-column align="center" prop="loc" label="物资名称"></el-table-column>
						<el-table-column align="center" prop="userName" label="记录人员"></el-table-column>
						<el-table-column align="center" label="入/出库类型">
							<template slot-scope="scope">
								<el-tag v-if="scope.row.resl == '入库'">入库</el-tag>
								<el-tag type="danger" v-if="scope.row.resl == '出库'">出库</el-tag>
							</template>
						</el-table-column>
						<el-table-column align="center" label="操作处理">
							<template slot-scope="scope">
								<el-button v-if="userType == 0" icon="el-icon-edit" disabled
										type="primary" size="mini" @click="showUpdWin(scope.row)"></el-button>
								<el-button v-if="userType == 0" icon="el-icon-delete" disabled
									type="danger" size="mini" @click="delCheckInfo(scope.row.id)"></el-button>
								<el-button v-if="userType == 1" icon="el-icon-edit"
										type="primary" size="mini" @click="showUpdWin(scope.row)"></el-button>
								<el-button v-if="userType == 1" icon="el-icon-delete"
									type="danger" size="mini" @click="delCheckInfo(scope.row.id)"></el-button>
							</template>
						</el-table-column>
				</el-table>
				<el-pagination v-if="pageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
					@current-change="handleCurrentChange" :current-page="pageIndex" :page-sizes="[10, 20, 50]"
					:page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="totalInfo">
				</el-pagination>
			</div>
        </el-card>

        <el-dialog title="添加信息" width="600px" :visible.sync="showAddFlag">
			<el-form label-width="90px" :model="checkForm">
				<el-form-item label="入/出库类型">
					<el-radio-group v-model="checkForm.resl">
						<el-radio label="入库" value="入库"></el-radio>
						<el-radio label="出库" value="出库"></el-radio>
					</el-radio-group>
				</el-form-item>
				<el-form-item label="物资名称">
					<el-input v-model="checkForm.loc" 
						placeholder="请输入物资名称…" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item label="入/出库详情">
					<el-input type="textarea" v-model="checkForm.detail" 
						:rows="6" placeholder="请输入入/出库详情…" autocomplete="off"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showAddFlag = false">取 消</el-button>
				<el-button type="primary" @click="addCheckInfo()">确 定</el-button>
			</div>
		</el-dialog>

        <el-dialog title="修改信息" width="600px" :visible.sync="showUpdFlag">
			<el-form label-width="90px" :model="checkForm">
				<el-form-item label="入/出库类型">
					<el-radio-group v-model="checkForm.resl">
						<el-radio label="入库" value="入库"></el-radio>
						<el-radio label="出库" value="出库"></el-radio>
					</el-radio-group>
				</el-form-item>
				<el-form-item label="物资名称">
					<el-input v-model="checkForm.loc" 
						placeholder="请输入物资名称…" autocomplete="off"></el-input>
				</el-form-item>
				<el-form-item label="入/出库详情">
					<el-input type="textarea" v-model="checkForm.detail" 
						:rows="6" placeholder="请输入入/出库详情…" autocomplete="off"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showUpdFlag = false">取 消</el-button>
				<el-button type="primary" @click="updCheckInfo()">确 定</el-button>
			</div>
		</el-dialog>
    </div>
</template>

<style>

</style>

<script>

	import { 
		getPageChecks,
		addChecks,
		updChecks,
		delChecks 
	} from '../../api/index.js'

    import {getLoginUser} from "../../api";
	import store from "../../store";

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
				checkForm: {
					id: "",
					resl: "",
					loc: "",
					detail: "",
					token: this.$store.state.token
				},
                qryForm: {
					resl: "",
					loc: "",
				},
            }
        },
        methods: {
			getUserType(store) {
				
				let token = null;

				if(store.state.token){
					token = store.state.token;
				}else{

				token = sessionStorage.getItem("token");
					store.state.token = sessionStorage.getItem("token");
				}

				getLoginUser(token).then(resp =>{
					this.userType = !resp.data.type;
				});
				console.log(this.userType);
			},

			getPageInfo(pageIndex, pageSize) {

				getPageChecks(pageIndex, pageSize, this.$store.state.token, this.qryForm.resl, this.qryForm.loc).then(resp => {

					this.pageInfos = resp.data.data;
					this.pageIndex = resp.data.pageIndex;
					this.pageSize = resp.data.pageSize;
					this.pageTotal = resp.data.pageTotal;
					this.totalInfo = resp.data.count;

					this.loading = false;
				});
			},
            getPageLikeInfo() {
				getPageChecks(1, this.pageSize, this.$store.state.token, this.qryForm.resl, this.qryForm.loc).then(resp => {

					this.pageInfos = resp.data.data;
					this.pageIndex = resp.data.pageIndex;
					this.pageSize = resp.data.pageSize;
					this.totalInfo = resp.data.count;
					this.pageTotal = resp.data.pageTotal;
					this.loading = false;
				});
			},
			handleSizeChange(pageSize) {

				this.getPageInfo(this.pageIndex, pageSize, this.$store.state.token, this.qryForm.resl, this.qryForm.loc);
			},
			handleCurrentChange(pageIndex) {

				this.getPageInfo(pageIndex, this.pageSize, this.$store.state.token, this.qryForm.resl, this.qryForm.loc);
			},
			initCheckForm() {

				this.checkForm = {
					id: "",
					resl: "",
					loc: "",
					detail: "",
					token: this.$store.state.token
				}
			},
            showAddWin() {

				this.initCheckForm();
				this.showAddFlag = true;
			},
			showUpdWin(row) {

				this.checkForm = row;
				
				this.showUpdFlag = true;
			},
			addCheckInfo(){

				addChecks(this.checkForm).then(resp =>{

					this.$message({
						message: resp.msg,
						type: 'success'
					});

					this.getPageInfo(1, this.pageSize);

					this.showAddFlag = false;
				});
			},
			updCheckInfo(){

				updChecks(this.checkForm).then(resp =>{

					this.$message({
						message: resp.msg,
						type: 'success'
					});

					this.getPageInfo(1, this.pageSize);

					this.showUpdFlag = false;
				});
			},
			delCheckInfo(id){

				this.$confirm('即将删除相关信息, 是否继续?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(() => {
					
					delChecks(id).then(resp =>{
					
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
			this.getUserType(store);
			this.getPageInfo(1, this.pageSize);
        }
    }
</script>
