<template>
    <div class="fater-body-show">
        <el-row :gutter="15">
            <el-col :span="6">
                <div class="fater-statis confirm">
                    <div class="fater-statis-desc">累计确诊</div>
                    <div class="fater-statis-num">{{ nows.confirm }}</div>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="fater-statis heal">
                    <div class="fater-statis-desc">累计治愈</div>
                    <div class="fater-statis-num">{{ nows.heal }}</div>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="fater-statis dead">
                    <div class="fater-statis-desc">累计死亡</div>
                    <div class="fater-statis-num">{{ nows.dead }}</div>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="fater-statis confirm2">
                    <div class="fater-statis-desc">当前确诊</div>
                    <div class="fater-statis-num">{{ nows.nowConfirm }}</div>
                </div>
            </el-col>
        </el-row>
        <el-row :gutter="15">
            <el-col :span="12">
                <el-card shadow="never">
                    <div slot="header"><strong>七日累计变化</strong></div>
                    <div ref="linesImgs" style="width: 100%;height: 300px;"></div>
                </el-card>
            </el-col>
            <el-col :span="12">
                <el-card shadow="never">
                    <div slot="header"><strong>七日确诊情况</strong></div>
                    <div ref="barImgs" style="width: 100%;height: 300px;"></div>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="15">
            <el-col :span="9">
                <el-card shadow="never">
                    <div slot="header"><strong>求助列表</strong></div>
                    <div>
                        <el-timeline>
                            <el-timeline-item color="#b3ffab" v-for="(item, index) in notices" :key="index"
                                :timestamp="item.createTime" placement="top">
                                <el-card>
                                    <h4 style="font-size: 16px; line-height:28px;margin-bottom:15px;">{{ item.title }}</h4>
                                    <p style="font-size: 14px; line-height:28px;">{{ item.detail }}</p>
                                </el-card>
                            </el-timeline-item>
                        </el-timeline>
                    </div>
                </el-card>
            </el-col>
            <el-col :span="15">
                <el-card shadow="never">
                        <div class="block">
                            <el-carousel  height="400px">
                                <el-carousel-item v-for="item in imgList" :key="item">
                                    <img :src="item">
                                </el-carousel-item>
                            </el-carousel>
                        </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>

import { 
        getNoticeList ,
        getTopTotal,
        getNowTotal,
        getNow
      } from '../../api/index.js';

import * as echarts from "echarts";

export default {
    data(){

        return {

            notices: [],
            nows: {},
            imgList: [
                require('../../assets/1.jpg'),
                require('../../assets/2.jpg'),
                require('../../assets/3.jpg')
            ],
            topTotals: {
                dateItems: [],
                confirmList: [],
                healList: [],
                deadList: [],
            },
            nowTotals: {
                dateItems: [],
                dataList: [],
            },
        }
    },
    methods: {

        drawBars(){

            let barImgs = echarts.init(this.$refs.barImgs);

            barImgs.setOption({
                            tooltip: {
                                trigger: 'axis'
                            },
                            grid: {
                                left: '3%',
                                right: '4%',
                                bottom: '3%',
                                containLabel: true
                            },
                            xAxis: {
                                data: this.nowTotals.dateItems
                            },
                            yAxis: {},
                            series: [
                                {
                                    type: 'bar',
                                    data: this.nowTotals.dataList
                                }
                            ]
                        });
        },
        drawLines(){

            let linesImgs = echarts.init(this.$refs.linesImgs);

            linesImgs.setOption({
                            tooltip: {
                                trigger: 'axis'
                            },
                            grid: {
                                left: '3%',
                                right: '4%',
                                bottom: '3%',
                                containLabel: true
                            },
                            xAxis: {
                                type: 'category',
                                boundaryGap: false,
                                data: this.topTotals.dateItems
                            },
                            yAxis: {
                                type: 'value'
                            },
                            series: [
                                {
                                    name: '累计确诊',
                                    type: 'line',
                                    data: this.topTotals.confirmList
                                },
                                {
                                    name: '累计治愈',
                                    type: 'line',
                                    data: this.topTotals.healList
                                },
                                {
                                    name: '累计死亡',
                                    type: 'line',
                                    data: this.topTotals.deadList
                                }
                            ]
                        });                
        },
        initPage(){

            getNoticeList().then(resp =>{

                this.notices = resp.data;
            });
            getTopTotal().then(resp =>{

                resp.data.forEach((item) =>{

                                    this.topTotals.dateItems.push(item.date);
                                    this.topTotals.confirmList.push(item.confirm);
                                    this.topTotals.healList.push(item.heal);
                                    this.topTotals.deadList.push(item.dead);
                                })

                this.topTotals.dateItems = this.topTotals.dateItems.reverse();
                this.topTotals.confirmList = this.topTotals.confirmList.reverse();
                this.topTotals.healList = this.topTotals.healList.reverse();
                this.topTotals.deadList = this.topTotals.deadList.reverse();

                this.drawLines();
            });
            getNowTotal().then(resp =>{

                resp.data.forEach((item) =>{

                                    this.nowTotals.dateItems.push(item.date);
                                    this.nowTotals.dataList.push(item.nowConfirm);
                                });
                
                this.nowTotals.dateItems = this.nowTotals.dateItems.reverse();
                this.nowTotals.dataList = this.nowTotals.dataList.reverse();

                this.drawBars();
            });
            
            getNow().then(resp =>{

                this.nows = resp.data;
            });
        }
    },
    mounted(){

        this.initPage();
    }
}

</script>

<style>
  .el-carousel__item img {
      height: 100%;
      width: 100%;
    margin: 0;
  }
</style>