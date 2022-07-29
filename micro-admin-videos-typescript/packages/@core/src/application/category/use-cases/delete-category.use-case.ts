import { CategoryRepository } from "../../../domain/category/repository/category.repository";
import {default as DefaultUseCase} from "../../use-case";

export namespace DeleteCategoryUseCase{
  export class UseCase implements DefaultUseCase<Input, Output> {
    constructor(private categoryRepository: CategoryRepository.Repository) {}
  
    async execute(input: Input): Promise<Output> {
      await this.categoryRepository.delete(input.id);
    }
  }
  
  export type Input = {
    id: string;
  };
  
  type Output = void;
}


export default DeleteCategoryUseCase;