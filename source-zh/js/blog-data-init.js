/**
 * 博客数据初始化脚本 - 从 JSON 文件加载文章/标签/分类数据
 */
(function() {
  'use strict';
  
  function loadBlogDataFromJSON() {
    fetch('/js/blog-data.json')
      .then(response => {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(data => {
        // 注入到全局变量
        window.postsData = data.posts || [];
        window.tagsData = data.tags || [];
        window.categoriesData = data.categories || [];
        
        console.log(`✅ 博客数据加载成功：`);
        console.log(`   📝 ${window.postsData.length} 篇文章`);
        console.log(`   🏷️ ${window.tagsData.length} 个标签`);
        console.log(`   📁 ${window.categoriesData.length} 个分类`);
        
        // 触发自定义事件，通知其他组件数据已就绪
        document.dispatchEvent(new CustomEvent('blogDataLoaded', { detail: data }));
      })
      .catch(error => {
        console.warn('⚠️ 博客数据加载失败:', error.message);
        console.warn('   这可能是因为博客数据文件尚未生成，请运行 hexo generate');
        
        // 设置空数据作为后备
        window.postsData = [];
        window.tagsData = [];
        window.categoriesData = [];
      });
  }
  
  // 页面加载完成后执行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadBlogDataFromJSON);
  } else {
    loadBlogDataFromJSON();
  }
})();
