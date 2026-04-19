<template>
  <div class="w-full pb-12" data-purpose="dashboard-main-content">
    
    <!-- BEGIN: JobSelectionSection -->
    <section id="job-selection" class="py-6 px-4 max-w-7xl mx-auto" data-purpose="job-selection-grid">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-slate-800 mb-4">选择您的目标职位</h2>
        <p class="text-slate-500">针对性模拟面试，覆盖核心技术栈，助您做好万全准备</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div 
          v-for="role in roles" 
          :key="role.id"
          @click="startInterview(role)"
          class="group relative bg-white p-8 rounded-2xl border border-slate-200 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl hover:border-[#0066CC] cursor-pointer" 
        >
          <div class="w-14 h-14 bg-blue-50 text-[#0066CC] rounded-xl flex items-center justify-center mb-6 group-hover:bg-[#0066CC] group-hover:text-white transition-colors duration-300">
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-slate-800 mb-3">{{ role.name }}</h3>
          <p class="text-slate-600 leading-relaxed mb-6 h-12 overflow-hidden text-sm">
            {{ role.desc }}
          </p>
          <div class="flex items-center text-sm font-semibold text-[#0066CC]">
            进入模拟 <svg class="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
          </div>
        </div>
      </div>
    </section>
    <!-- END: JobSelectionSection -->

    <!-- 面试参数设置弹窗 -->
    <InterviewSettingsDialog 
      ref="settingsDialogRef" 
      :role-name="selectedRole?.name" 
      :role-key="selectedRole?.key"
      @confirm="onSettingsConfirm"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import InterviewSettingsDialog from '@/components/business/InterviewSettingsDialog.vue'

const router = useRouter()
const roles = ref([])
const settingsDialogRef = ref(null)
const selectedRole = ref(null)

onMounted(async () => {
  try {
    const { data } = await api.get('/interview/roles')
    roles.value = data
  } catch (err) {
    console.error('Failed to fetch roles:', err)
  }
})

const startInterview = (role) => {
  selectedRole.value = role
  settingsDialogRef.value.open(role.key)
}

const onSettingsConfirm = async (settings) => {
  try {
    const { data } = await api.post('/interview/start', {
      role: selectedRole.value.name,
      ...settings
    })
    router.push({ 
      name: 'InterviewRoom', 
      params: { role: selectedRole.value.name },
      query: { interviewId: data.id }
    })
  } catch (err) {
    console.error('Failed to start interview:', err)
  }
}
</script>

<style scoped>
svg { display: block; }
</style>