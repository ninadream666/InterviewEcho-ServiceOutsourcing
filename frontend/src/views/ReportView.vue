<template>
  <div class="bg-transparent w-full">
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 min-h-[600px] w-full p-8 md:p-12 max-w-7xl mx-auto mt-6 mb-12">
      
      <!-- 头部信息 -->
      <div class="mb-8 border-b border-gray-200 pb-6 flex justify-between items-end">
        <div>
          <h1 class="text-3xl font-extrabold text-gray-900 tracking-tight">面试评估报告</h1>
          <p class="text-gray-500 mt-2 text-sm" v-if="report">
            岗位：{{ report.role }} | 评估时间：{{ formatDateTime(report.created_at) }} | 综合得分：<span class="text-[#0066CC] font-bold">{{ Number(report.total_score || 0).toFixed(1) }}</span>
          </p>
        </div>
        <button @click="router.push('/profile')" class="text-sm font-medium text-[#0066CC] hover:underline decoration-2 underline-offset-4 cursor-pointer">
          返回历史大盘
        </button>
      </div>

      <div v-if="report" class="space-y-12">
        <!-- 主体区域：左右分栏 -->
        <div class="flex flex-col md:flex-row gap-10">
          
          <!-- 左侧：雷达图能力可视化 (5/12) -->
          <div class="w-full md:w-5/12 flex flex-col items-center">
            <h3 class="text-lg font-bold text-gray-800 mb-4 self-start">多维度能力图谱</h3>
            <div class="w-full h-[350px] bg-gray-50 rounded-lg p-4 border border-gray-100 flex items-center justify-center">
              <RadarChart :stats="{
                technical_depth: report.content_score,
                communication: report.expression_score,
                business_scenario: report.business_scenario_score,
                problem_solving: report.problem_solving_score
              }" />
            </div>
          </div>

          <!-- 右侧：文字评价与建议 (7/12) -->
          <div class="w-full md:w-7/12 space-y-6">
            
            <!-- 核心优势 -->
            <div>
              <h3 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
                <span class="w-1.5 h-5 bg-green-500 rounded-full mr-2"></span>
                核心优势
              </h3>
              <div class="bg-green-50/50 p-4 rounded-lg border border-green-100">
                <ul class="list-disc list-inside text-gray-600 text-sm leading-relaxed space-y-2 ml-1">
                  <li v-for="(highlight, idx) in parsedReportData.highlights" :key="idx">{{ highlight }}</li>
                </ul>
              </div>
            </div>

            <!-- 改进建议 -->
            <div>
              <h3 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
                <span class="w-1.5 h-5 bg-orange-500 rounded-full mr-2"></span>
                待提升项
              </h3>
              <div class="bg-orange-50/50 p-4 rounded-lg border border-orange-100">
                <ul class="list-disc list-inside text-gray-600 text-sm leading-relaxed space-y-2 ml-1">
                  <li v-for="(weakness, idx) in parsedReportData.weaknesses" :key="idx">{{ weakness }}</li>
                </ul>
              </div>
            </div>

            <!-- 提升建议 -->
            <div>
              <h3 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
                <span class="w-1.5 h-5 bg-[#0066CC] rounded-full mr-2"></span>
                提升建议
              </h3>
              <div class="bg-blue-50/50 p-4 rounded-lg border border-blue-100">
                <p class="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap ml-1">
                  {{ report.recommendations || report.improvement_suggestions || parsedReportData.recommendations || '暂无具体建议，请继续保持练习。' }}
                </p>
              </div>
            </div>

          </div>
        </div>

        <!-- 🌟 V2: 表达能力深度诊断 🌟 -->
        <div v-if="report.expression_metrics" class="pt-10 border-t border-gray-200">
          <div class="mb-8">
            <h1 class="text-2xl font-extrabold text-gray-900 tracking-tight">表达沟通专项分析</h1>
            <p class="text-gray-500 mt-2 text-sm">基于您的语音与语义特征生成的深度声学诊断报告</p>
          </div>

          <div class="flex flex-col md:flex-row gap-10">
            <!-- 左侧：表达图表可视化 (5/12) -->
            <div class="w-full md:w-5/12 flex flex-col items-center">
              <h3 class="text-lg font-bold text-gray-800 mb-4 self-start">表达综合雷达</h3>
              <div class="w-full h-[250px] bg-gray-50 rounded-lg p-4 border border-gray-100 flex items-center justify-center mb-6">
                <RadarChart 
                  :indicators="[
                    { name: '语速节奏', max: 100 },
                    { name: '语义清晰度', max: 100 },
                    { name: '用词自信度', max: 100 }
                  ]"
                  :dataValues="[report.speech_rate_score || 0, report.clarity_score || 0, report.confidence_score || 0]"
                  seriesName="表达能力诊断"
                />
              </div>
              
              <h3 class="text-lg font-bold text-gray-800 mb-4 self-start">语速波动曲线 (wpm)</h3>
              <div class="w-full h-[220px] bg-gray-50 rounded-lg p-2 border border-gray-100">
                <ExpressionLineChart :data="report.expression_metrics.per_message" />
              </div>
            </div>

            <!-- 右侧：文字评价与口头禅分析 (7/12) -->
            <div class="w-full md:w-7/12 space-y-6">
              <!-- 口头禅监控 -->
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
                  <span class="w-1.5 h-5 bg-rose-500 rounded-full mr-2"></span>
                  习惯填充词监控 (Filler Words)
                </h3>
                <div class="bg-rose-50/30 p-4 rounded-lg border border-rose-100 min-h-[5rem] flex items-center">
                  <div v-if="report.expression_metrics.metrics_summary.top_filler_words && report.expression_metrics.metrics_summary.top_filler_words.length > 0" class="flex flex-wrap gap-2">
                    <span 
                      v-for="(filler, index) in report.expression_metrics.metrics_summary.top_filler_words" 
                      :key="index"
                      class="rounded px-2.5 py-1 bg-white border border-rose-200 text-rose-700 font-medium shadow-sm"
                      :style="{ fontSize: `${0.8 + filler.count * 0.05}rem` }"
                    >
                      {{ filler.word }} <span class="text-xs text-rose-400 ml-1">x{{ filler.count }}</span>
                    </span>
                  </div>
                  <div v-else class="text-sm text-emerald-600 font-medium w-full text-center">
                    表现极佳，未检测到高频无意义口头禅！
                  </div>
                </div>
              </div>

              <!-- 语速建议 -->
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
                  <span class="w-1.5 h-5 bg-blue-400 rounded-full mr-2"></span>
                  语速节奏评价
                </h3>
                <div class="bg-blue-50/50 p-4 rounded-lg border border-blue-100">
                  <p class="text-gray-600 text-sm leading-relaxed ml-1">
                    {{ report.expression_metrics.feedback.speech_rate }}
                  </p>
                </div>
              </div>

              <!-- 清晰度建议 -->
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
                  <span class="w-1.5 h-5 bg-blue-500 rounded-full mr-2"></span>
                  逻辑清晰度评价
                </h3>
                <div class="bg-blue-50/50 p-4 rounded-lg border border-blue-100">
                  <p class="text-gray-600 text-sm leading-relaxed ml-1">
                    {{ report.expression_metrics.feedback.clarity }}
                  </p>
                </div>
              </div>

              <!-- 自信度建议 -->
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
                  <span class="w-1.5 h-5 bg-[#0066CC] rounded-full mr-2"></span>
                  专业自信度评价
                </h3>
                <div class="bg-blue-50/50 p-4 rounded-lg border border-blue-100">
                  <p class="text-gray-600 text-sm leading-relaxed ml-1">
                    {{ report.expression_metrics.feedback.confidence }}
                  </p>
                </div>
              </div>

            </div>
          </div>
        </div>
        <!-- 🌟 V2 End 🌟 -->

      </div>
      
      <!-- 加载占位 -->
      <div v-else class="text-center text-gray-500 py-20 flex flex-col items-center justify-center">
        <svg class="w-10 h-10 text-gray-300 mb-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        <span>正在为您加载专业评估报告...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import { ElMessage } from 'element-plus'
import RadarChart from '@/components/analytics/RadarChart.vue'
import ExpressionLineChart from '@/components/analytics/ExpressionLineChart.vue'

const route = useRoute()
const router = useRouter()
const report = ref(null)
const loading = ref(false)

onMounted(async () => {
  if (history.state && history.state.evaluation) {
    report.value = history.state.evaluation
    return
  }

  const evalId = route.params.id
  if (evalId) {
    loading.value = true
    try {
      const { data } = await api.get(`/interview/${evalId}/evaluation`)
      report.value = data
    } catch (err) {
      ElMessage.error('无法加载评估报告')
      router.push('/dashboard')
    } finally {
      loading.value = false
    }
  }
})

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
}

const parsedReportData = computed(() => {
  if (!report.value) return { highlights: [], weaknesses: [], recommendations: '' }
  
  if (report.value.report_json) {
    try {
      const data = typeof report.value.report_json === 'string' 
        ? JSON.parse(report.value.report_json) 
        : report.value.report_json
      return {
        highlights: data.highlights || data.strengths || [],
        weaknesses: data.weaknesses || [],
        recommendations: data.recommendations || data.improvement_suggestions || ''
      }
    } catch(e) {
      return { highlights: ['评估数据解析异常'], weaknesses: [], recommendations: '' }
    }
  }
  
  return {
    highlights: report.value.highlights || report.value.strengths || [],
    weaknesses: report.value.weaknesses || [],
    recommendations: report.value.recommendations || report.value.improvement_suggestions || ''
  }
})
</script>