<template>
    <div class="fater-body-show">
        <el-card shadow="never">
			<div slot="header">
				<strong>信息查询</strong>
			</div>
			<div>
				<el-form :inline="true" :model="qryForm">
					<el-form-item >
						<el-input v-model="qryForm.name"
							placeholder="输入物资名称…"
							autocomplete="off"></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.card"
							placeholder="输入物资编号…"
							autocomplete="off"></el-input>
					</el-form-item>
					<el-form-item >
						<el-input v-model="qryForm.address"
							placeholder="输入物资来源…"
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
						<el-table-column align="center" prop="name" label="物资名称"></el-table-column>
						<el-table-column align="center" prop="card" label="物资编号"></el-table-column>
						<el-table-column align="center" prop="phone" label="数量"></el-table-column>
						<el-table-column align="center" prop="address" label="来源"></el-table-column>
						<el-table-column align="center" prop="vaccinateTime" label="入库时间"></el-table-column>
						<el-table-column align="center" prop="vaccinateNo" label="类别"></el-table-column>
						<el-table-column align="center" prop="uName" label="记录人员"></el-table-column>
						<el-table-column align="center" label="操作处理">
							<template slot-scope="scope">
								<el-button v-if="userType == 0" icon="el-icon-edit" disabled
										type="primary" size="mini" @click="showUpdWin(scope.row)"></el-button>
								<el-button v-if="userType == 0" icon="el-icon-delete" disabled
									type="danger" size="mini" @click="delVaccinateInfo(scope.row.id)"></el-button>
								<el-button v-if="userType == 1" icon="el-icon-edit"
										type="primary" size="mini" @click="showUpdWin(scope.row)"></el-button>
								<el-button v-if="userType == 1" icon="el-icon-delete"
									type="danger" size="mini" @click="delVaccinateInfo(scope.row.id)"></el-button>
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
			<el-form label-width="90px" :model="vaccinateForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="物资名称">
							<el-input v-model="vaccinateForm.name" 
								placeholder="请输入物资名称…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="物资编号">
							<el-input v-model="vaccinateForm.card" 
								placeholder="请输入物资编号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="类别">
							<el-select style="width:100%"
								v-model="vaccinateForm.vaccinateNo" placeholder="请选择类别">
								<el-option label="医护用品" value="医护用品"></el-option>
								<el-option label="食品饮品" value="食品饮品"></el-option>
								<el-option label="其他" value="其他"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="入库时间">
							<el-date-picker style="width:100%"
								v-model="vaccinateForm.vaccinateTime" type="date"
								value-format="yyyy-MM-dd"></el-date-picker>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="数量">
							<el-input v-model="vaccinateForm.phone" 
								placeholder="请输入物资数量…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="来源">
							<el-input  v-model="vaccinateForm.address" 
								placeholder="请输入物资来源…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showAddFlag = false">取 消</el-button>
				<el-button type="primary" @click="addVaccinateInfo()">确 定</el-button>
			</div>
		</el-dialog>

        <el-dialog title="修改信息" width="600px" :visible.sync="showUpdFlag">
			<el-form label-width="90px" :model="vaccinateForm">
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="物资名称">
							<el-input v-model="vaccinateForm.name" 
								placeholder="请输入物资名称…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="物资编号">
							<el-input v-model="vaccinateForm.card" 
								placeholder="请输入物资编号…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="类别">
							<el-select style="width:100%"
								v-model="vaccinateForm.vaccinateNo" placeholder="请选择类别">
								<el-option label="医护用品" value="医护用品"></el-option>
								<el-option label="食品饮品" value="食品饮品"></el-option>
								<el-option label="其他" value="其他"></el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="入库时间">
							<el-date-picker style="width:100%"
								v-model="vaccinateForm.vaccinateTime" type="date"
								value-format="yyyy-MM-dd"></el-date-picker>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="15">
					<el-col :span="12">
						<el-form-item label="数量">
							<el-input v-model="vaccinateForm.phone" 
								placeholder="请输入物资数量…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="来源">
							<el-input  v-model="vaccinateForm.address" 
								placeholder="请输入物资来源…" autocomplete="off"></el-input>
						</el-form-item>
					</el-col>
				</el-row>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="showUpdFlag = false">取 消</el-button>
				<el-button type="primary" @click="updVaccinateInfo()">确 定</el-button>
			</div>
		</el-dialog>
    </div>
</template>

<style>

</style>

<script>

	import { 
		getPageVaccinates,
		addVaccinates,
		updVaccinates,
		delVaccinates 
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
				vaccinateForm: {
					id: "",
					name: "",
					card: "",
					phone: "",
					address: "",
					vaccinateNo: "",
					vaccinateTime: "",
					token: this.$store.state.token
				},
                qryForm: {
					name: "",
					card: "",
					phone: "",
					address: "",
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

				getPageVaccinates(pageIndex, pageSize, this.$store.state.token, this.qryForm.name, this.qryForm.card, 
							this.qryForm.phone, this.qryForm.address).then(resp => {

					this.pageInfos = resp.data.data;
					this.pageIndex = resp.data.pageIndex;
					this.pageSize = resp.data.pageSize;
					this.pageTotal = resp.data.pageTotal;
					this.totalInfo = resp.data.count;

					this.loading = false;
				});
			},
            getPageLikeInfo() {
				getPageVaccinates(1, this.pageSize, this.$store.state.token, this.qryForm.name, this.qryForm.card, 
							this.qryForm.phone, this.qryForm.address).then(resp => {

					this.pageInfos = resp.data.data;
					this.pageIndex = resp.data.pageIndex;
					this.pageSize = resp.data.pageSize;
					this.totalInfo = resp.data.count;
					this.pageTotal = resp.data.pageTotal;
					this.loading = false;
				});
			},
			handleSizeChange(pageSize) {

				this.getPageInfo(this.pageIndex, pageSize, this.$store.state.token, this.qryForm.name, this.qryForm.card, 
							this.qryForm.phone, this.qryForm.address);
			},
			handleCurrentChange(pageIndex) {

				this.getPageInfo(pageIndex, this.pageSize, this.$store.state.token, this.qryForm.name, this.qryForm.card, 
							this.qryForm.phone, this.qryForm.address);
			},
			initVaccinateForm() {

				this.vaccinateForm = {
					id: "",
					name: "",
					card: "",
					phone: "",
					address: "",
					vaccinateNo: "",
					vaccinateTime: "",
					token: this.$store.state.token
				}
			},
            showAddWin() {

				this.initVaccinateForm();
				this.showAddFlag = true;
			},
			showUpdWin(row) {

				this.vaccinateForm = row;
				
				this.showUpdFlag = true;
			},
			addVaccinateInfo(){

				addVaccinates(this.vaccinateForm).then(resp =>{

					this.$message({
						message: resp.msg,
						type: 'success'
					});

					this.getPageInfo(1, this.pageSize);

					this.showAddFlag = false;
				});
			},
			updVaccinateInfo(){

				updVaccinates(this.vaccinateForm).then(resp =>{

					this.$message({
						message: resp.msg,
						type: 'success'
					});

					this.getPageInfo(1, this.pageSize);

					this.showUpdFlag = false;
				});
			},
			delVaccinateInfo(id){

				this.$confirm('即将删除相关信息, 是否继续?', '提示', {
					confirmButtonText: '确定',
					cancelButtonText: '取消',
					type: 'warning'
				}).then(() => {
					
					delVaccinates(id).then(resp =>{
					
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
