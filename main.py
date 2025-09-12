
import torch
import torchaudio
import torchvision


def basic_calculation(a: int, b: int) -> torch.Tensor:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tensor_a = torch.arange(start=1, end=a + 1).unsqueeze(0)
    tensor_b = torch.arange(start=1, end=b + 1).unsqueeze(0)
    tensor_product = torch.matmul(tensor_a.T, tensor_b).to(device)
    return tensor_product

print(torch.cuda.is_available())
print("torch.__version__:", torch.__version__)
print("torchvision.__version__:", torchvision.__version__)
print("torchaudio.__version__:", torchaudio.__version__)
print("torch.cuda.is_available:", torch.cuda.is_available())
print()
for i in range(torch.cuda.device_count()):
    print("Device", i, ": ", end="")
    print(torch.cuda.get_device_properties(i))
print()
print("Test calculation")
print(basic_calculation(2, 3))