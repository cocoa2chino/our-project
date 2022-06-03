<template>
    <div class="fater-body-show">

        <el-card shadow="never">
			<div slot="header">
				<el-button type="primary" size="mini"
						@click="initData()">数据同步</el-button>
			</div>
			<div>
				<el-table v-loading="loading" 
					element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading"
					element-loading-background="rgba(124, 124, 124, 0.8)" :data="pageInfos" border>
						<el-table-column align="center" type="index"></el-table-column>
						<el-table-column align="center" prop="createTime" label="统计时间"></el-table-column>
						<el-table-column align="center" prop="confirm" label="累计确诊"></el-table-column>
						<el-table-column align="center" prop="dead" label="累计死亡"></el-table-column>
						<el-table-column align="center" prop="heal" label="累计治愈"></el-table-column>
						<el-table-column align="center" prop="nowConfirm" label="当日确诊"></el-table-column>
				</el-table>
				<el-pagination v-if="pageTotal > 1" style="margin-top: 15px;" @size-change="handleSizeChange"
					@current-change="handleCurrentChange" :current-page="pageIndex" :page-sizes="[10, 20, 50]"
					:page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="totalInfo">
				</el-pagination>
			</div>
        </el-card>
    </div>
</template>

<style>

</style>

<script>

	import { 
		getPageStatistics,
		initStatistics,
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
            }
        },
        methods: {
			getPageInfo(pageIndex, pageSize) {

				getPageStatistics(pageIndex, pageSize).then(resp => {

					this.pageInfos = resp.data.data;
					this.pageIndex = resp.data.pageIndex;
					this.pageSize = resp.data.pageSize;
					this.pageTotal = resp.data.pageTotal;
					this.totalInfo = resp.data.count;

					this.loading = false;
				});
			},
			handleSizeChange(pageSize) {

				this.getPageInfo(this.pageIndex, pageSize);
			},
			handleCurrentChange(pageIndex) {

				this.getPageInfo(pageIndex, this.pageSize);
			},
			initData(){

				initStatistics().then(resp =>{

					this.$message({
						message: resp.msg,
						type: 'success'
					});

					this.getPageInfo(1, this.pageSize);
				});
			}
        },
        mounted(){
			
			this.getPageInfo(1, this.pageSize);
        }
    }
</script>
