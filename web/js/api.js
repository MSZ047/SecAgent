export async function validateUrl(url) {
  try {
    const result = await eel.validate_url(url)();
    return result;
  } catch (error) {
    return {
      ok: false,
      message: "URL 校验失败，请检查 Eel 是否正常启动。",
    };
  }
}

export async function analyzeUrl(url) {
  try {
    const result = await eel.analyze_url(url)();
    return result;
  } catch (error) {
    return {
      status: "error",
      message: "分析请求失败，请检查 Python 侧服务。",
    };
  }
}